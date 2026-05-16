"""
Model Context Protocol (MCP) Server Implementation
Latest standard for agent-to-agent communication and tool sharing

MCP enables:
- Tool discovery and invocation
- Resource sharing across agents
- Prompt templates
- Sampling/generation requests
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import inspect

from backend.python.utils.logger import get_logger

logger = get_logger(__name__)


class MCPMessageType(Enum):
    """MCP message types"""
    INITIALIZE = "initialize"
    TOOLS_LIST = "tools/list"
    TOOLS_CALL = "tools/call"
    RESOURCES_LIST = "resources/list"
    RESOURCES_READ = "resources/read"
    PROMPTS_LIST = "prompts/list"
    PROMPTS_GET = "prompts/get"
    SAMPLING_CREATE = "sampling/createMessage"


@dataclass
class MCPTool:
    """MCP Tool definition"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    handler: Callable
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MCPResource:
    """MCP Resource definition"""
    uri: str
    name: str
    description: str
    mime_type: str
    content: Union[str, bytes, Callable]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MCPPrompt:
    """MCP Prompt template"""
    name: str
    description: str
    arguments: List[Dict[str, Any]]
    template: str


class MCPServer:
    """
    Model Context Protocol Server

    Provides tools, resources, and prompts to MCP clients (agents)
    Enables efficient inter-agent communication
    """

    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, MCPTool] = {}
        self.resources: Dict[str, MCPResource] = {}
        self.prompts: Dict[str, MCPPrompt] = {}
        self._initialized = False
        logger.info(f"MCP Server '{name}' v{version} created")

    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        handler: Callable,
        **metadata
    ):
        """Register a tool that agents can invoke"""
        tool = MCPTool(
            name=name,
            description=description,
            input_schema=input_schema,
            handler=handler,
            metadata=metadata
        )
        self.tools[name] = tool
        logger.info(f"Registered tool: {name}")

    def tool(self, name: str, description: str, input_schema: Dict[str, Any]):
        """Decorator for registering tools"""
        def decorator(func: Callable):
            self.register_tool(name, description, input_schema, func)
            return func
        return decorator

    def register_resource(
        self,
        uri: str,
        name: str,
        description: str,
        mime_type: str,
        content: Union[str, bytes, Callable],
        **metadata
    ):
        """Register a resource that agents can access"""
        resource = MCPResource(
            uri=uri,
            name=name,
            description=description,
            mime_type=mime_type,
            content=content,
            metadata=metadata
        )
        self.resources[uri] = resource
        logger.info(f"Registered resource: {uri}")

    def register_prompt(
        self,
        name: str,
        description: str,
        arguments: List[Dict[str, Any]],
        template: str
    ):
        """Register a prompt template"""
        prompt = MCPPrompt(
            name=name,
            description=description,
            arguments=arguments,
            template=template
        )
        self.prompts[name] = prompt
        logger.info(f"Registered prompt: {name}")

    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP message"""
        msg_type = message.get("method")
        msg_id = message.get("id")

        try:
            if msg_type == MCPMessageType.INITIALIZE.value:
                return await self._handle_initialize(msg_id, message.get("params", {}))

            elif msg_type == MCPMessageType.TOOLS_LIST.value:
                return await self._handle_tools_list(msg_id)

            elif msg_type == MCPMessageType.TOOLS_CALL.value:
                return await self._handle_tools_call(msg_id, message.get("params", {}))

            elif msg_type == MCPMessageType.RESOURCES_LIST.value:
                return await self._handle_resources_list(msg_id)

            elif msg_type == MCPMessageType.RESOURCES_READ.value:
                return await self._handle_resources_read(msg_id, message.get("params", {}))

            elif msg_type == MCPMessageType.PROMPTS_LIST.value:
                return await self._handle_prompts_list(msg_id)

            elif msg_type == MCPMessageType.PROMPTS_GET.value:
                return await self._handle_prompts_get(msg_id, message.get("params", {}))

            else:
                return self._error_response(msg_id, -32601, f"Method not found: {msg_type}")

        except Exception as e:
            logger.error(f"Error handling MCP message: {e}")
            return self._error_response(msg_id, -32603, str(e))

    async def _handle_initialize(self, msg_id: str, params: Dict) -> Dict:
        """Handle initialization request"""
        self._initialized = True
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": self.name,
                    "version": self.version
                },
                "capabilities": {
                    "tools": {"listChanged": True},
                    "resources": {"subscribe": True, "listChanged": True},
                    "prompts": {"listChanged": True}
                }
            }
        }

    async def _handle_tools_list(self, msg_id: str) -> Dict:
        """List available tools"""
        tools_list = [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema
            }
            for tool in self.tools.values()
        ]

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"tools": tools_list}
        }

    async def _handle_tools_call(self, msg_id: str, params: Dict) -> Dict:
        """Execute a tool"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name not in self.tools:
            return self._error_response(msg_id, -32602, f"Tool not found: {tool_name}")

        tool = self.tools[tool_name]

        try:
            # Execute tool handler
            if inspect.iscoroutinefunction(tool.handler):
                result = await tool.handler(**arguments)
            else:
                result = tool.handler(**arguments)

            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result) if not isinstance(result, str) else result
                        }
                    ]
                }
            }
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return self._error_response(msg_id, -32603, f"Tool execution failed: {str(e)}")

    async def _handle_resources_list(self, msg_id: str) -> Dict:
        """List available resources"""
        resources_list = [
            {
                "uri": resource.uri,
                "name": resource.name,
                "description": resource.description,
                "mimeType": resource.mime_type
            }
            for resource in self.resources.values()
        ]

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"resources": resources_list}
        }

    async def _handle_resources_read(self, msg_id: str, params: Dict) -> Dict:
        """Read a resource"""
        uri = params.get("uri")

        if uri not in self.resources:
            return self._error_response(msg_id, -32602, f"Resource not found: {uri}")

        resource = self.resources[uri]

        try:
            # Get content
            if callable(resource.content):
                if inspect.iscoroutinefunction(resource.content):
                    content = await resource.content()
                else:
                    content = resource.content()
            else:
                content = resource.content

            # Encode if bytes
            if isinstance(content, bytes):
                import base64
                content = base64.b64encode(content).decode('utf-8')

            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": resource.mime_type,
                            "text": content if isinstance(content, str) else json.dumps(content)
                        }
                    ]
                }
            }
        except Exception as e:
            logger.error(f"Resource read failed: {e}")
            return self._error_response(msg_id, -32603, f"Resource read failed: {str(e)}")

    async def _handle_prompts_list(self, msg_id: str) -> Dict:
        """List available prompts"""
        prompts_list = [
            {
                "name": prompt.name,
                "description": prompt.description,
                "arguments": prompt.arguments
            }
            for prompt in self.prompts.values()
        ]

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"prompts": prompts_list}
        }

    async def _handle_prompts_get(self, msg_id: str, params: Dict) -> Dict:
        """Get a prompt template"""
        prompt_name = params.get("name")
        arguments = params.get("arguments", {})

        if prompt_name not in self.prompts:
            return self._error_response(msg_id, -32602, f"Prompt not found: {prompt_name}")

        prompt = self.prompts[prompt_name]

        try:
            # Fill template with arguments
            filled_template = prompt.template.format(**arguments)

            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "description": prompt.description,
                    "messages": [
                        {
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": filled_template
                            }
                        }
                    ]
                }
            }
        except Exception as e:
            logger.error(f"Prompt get failed: {e}")
            return self._error_response(msg_id, -32603, f"Prompt get failed: {str(e)}")

    def _error_response(self, msg_id: str, code: int, message: str) -> Dict:
        """Create error response"""
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": code,
                "message": message
            }
        }

    async def start(self, host: str = "localhost", port: int = 8765):
        """Start MCP server (WebSocket)"""
        import websockets

        async def handler(websocket, path):
            logger.info(f"MCP client connected from {websocket.remote_address}")

            try:
                async for message in websocket:
                    request = json.loads(message)
                    response = await self.handle_message(request)
                    await websocket.send(json.dumps(response))
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
            finally:
                logger.info(f"MCP client disconnected")

        async with websockets.serve(handler, host, port):
            logger.info(f"MCP Server started on ws://{host}:{port}")
            await asyncio.Future()  # Run forever


# Global MCP server instance
_mcp_server: Optional[MCPServer] = None


def get_mcp_server() -> MCPServer:
    """Get global MCP server instance"""
    global _mcp_server
    if _mcp_server is None:
        _mcp_server = MCPServer("sentience-layer-mcp", "1.0.0")
    return _mcp_server
