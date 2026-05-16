"""
Model Context Protocol (MCP) Client
Allows agents to connect to MCP servers and use their tools/resources
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Callable
import websockets

from backend.python.utils.logger import get_logger

logger = get_logger(__name__)


class MCPClient:
    """
    MCP Client for agents to connect to MCP servers
    Enables tool discovery and invocation across agent boundaries
    """

    def __init__(self, server_url: str):
        self.server_url = server_url
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self._msg_id = 0
        self._pending_requests: Dict[str, asyncio.Future] = {}
        self._tools_cache: List[Dict] = []
        self._resources_cache: List[Dict] = []
        self._initialized = False

    async def connect(self):
        """Connect to MCP server"""
        try:
            self.ws = await websockets.connect(self.server_url)
            logger.info(f"Connected to MCP server: {self.server_url}")

            # Start message handler
            asyncio.create_task(self._message_handler())

            # Initialize
            await self.initialize()

        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            raise

    async def disconnect(self):
        """Disconnect from MCP server"""
        if self.ws:
            await self.ws.close()
            logger.info("Disconnected from MCP server")

    async def initialize(self):
        """Initialize MCP session"""
        response = await self._send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "clientInfo": {
                "name": "sentience-agent",
                "version": "1.0.0"
            }
        })
        self._initialized = True
        logger.info("MCP session initialized")
        return response

    async def list_tools(self) -> List[Dict]:
        """List available tools from server"""
        if self._tools_cache:
            return self._tools_cache

        response = await self._send_request("tools/list", {})
        self._tools_cache = response.get("tools", [])
        return self._tools_cache

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool on the server"""
        response = await self._send_request("tools/call", {
            "name": name,
            "arguments": arguments
        })

        # Extract content
        content = response.get("content", [])
        if content and len(content) > 0:
            text = content[0].get("text", "")
            try:
                return json.loads(text)
            except:
                return text
        return None

    async def list_resources(self) -> List[Dict]:
        """List available resources from server"""
        if self._resources_cache:
            return self._resources_cache

        response = await self._send_request("resources/list", {})
        self._resources_cache = response.get("resources", [])
        return self._resources_cache

    async def read_resource(self, uri: str) -> str:
        """Read a resource from server"""
        response = await self._send_request("resources/read", {"uri": uri})
        contents = response.get("contents", [])
        if contents and len(contents) > 0:
            return contents[0].get("text", "")
        return ""

    async def get_prompt(self, name: str, arguments: Dict[str, Any]) -> str:
        """Get a prompt template from server"""
        response = await self._send_request("prompts/get", {
            "name": name,
            "arguments": arguments
        })
        messages = response.get("messages", [])
        if messages and len(messages) > 0:
            return messages[0].get("content", {}).get("text", "")
        return ""

    async def _send_request(self, method: str, params: Dict) -> Dict:
        """Send request to server and wait for response"""
        if not self.ws:
            raise Exception("Not connected to MCP server")

        msg_id = str(self._msg_id)
        self._msg_id += 1

        request = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "method": method,
            "params": params
        }

        # Create future for response
        future = asyncio.Future()
        self._pending_requests[msg_id] = future

        # Send request
        await self.ws.send(json.dumps(request))

        # Wait for response
        try:
            response = await asyncio.wait_for(future, timeout=30.0)
            if "error" in response:
                raise Exception(f"MCP error: {response['error']}")
            return response.get("result", {})
        except asyncio.TimeoutError:
            del self._pending_requests[msg_id]
            raise Exception("MCP request timeout")

    async def _message_handler(self):
        """Handle incoming messages from server"""
        try:
            async for message in self.ws:
                data = json.loads(message)
                msg_id = data.get("id")

                if msg_id and msg_id in self._pending_requests:
                    future = self._pending_requests.pop(msg_id)
                    future.set_result(data)

        except Exception as e:
            logger.error(f"Message handler error: {e}")


class MCPToolRegistry:
    """
    Registry for MCP tools across multiple servers
    Allows agents to discover and use tools from any connected server
    """

    def __init__(self):
        self.clients: Dict[str, MCPClient] = {}
        self._all_tools: Dict[str, tuple] = {}  # tool_name -> (client, tool_info)

    async def register_server(self, name: str, url: str):
        """Register an MCP server"""
        client = MCPClient(url)
        await client.connect()
        self.clients[name] = client

        # Cache tools
        tools = await client.list_tools()
        for tool in tools:
            tool_name = tool["name"]
            self._all_tools[tool_name] = (client, tool)

        logger.info(f"Registered MCP server '{name}' with {len(tools)} tools")

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool by name (auto-routes to correct server)"""
        if tool_name not in self._all_tools:
            raise Exception(f"Tool not found: {tool_name}")

        client, tool_info = self._all_tools[tool_name]
        return await client.call_tool(tool_name, arguments)

    def list_all_tools(self) -> List[Dict]:
        """List all tools from all servers"""
        return [tool_info for _, tool_info in self._all_tools.values()]

    async def disconnect_all(self):
        """Disconnect from all servers"""
        for client in self.clients.values():
            await client.disconnect()


# Global registry
_mcp_registry: Optional[MCPToolRegistry] = None


def get_mcp_registry() -> MCPToolRegistry:
    """Get global MCP tool registry"""
    global _mcp_registry
    if _mcp_registry is None:
        _mcp_registry = MCPToolRegistry()
    return _mcp_registry
