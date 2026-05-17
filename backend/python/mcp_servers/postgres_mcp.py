"""
PostgreSQL MCP Server Implementation
Exposes SQL query, database table schema, and metadata discovery tools to agentic loops.
"""
import os
import sqlite3
import json
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class PostgresMcp:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.is_initialized = False
        self.db_path = ":memory:"
        self.conn = None

    def initialize(self) -> bool:
        """Initialize the simulated PostgreSQL/SQLite schema and seed telemetry datasets"""
        try:
            # Using an in-memory SQLite schema to simulate PostgreSQL robustly and cleanly
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            # Create active database tables for high-fidelity agentic queries
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cognitive_states (
                    id TEXT PRIMARY KEY,
                    agent_name TEXT,
                    state_key TEXT,
                    state_value TEXT,
                    confidence REAL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vault_metadata (
                    document_id TEXT PRIMARY KEY,
                    title TEXT,
                    file_type TEXT,
                    file_size TEXT,
                    status TEXT,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Seed telemetry records
            cursor.execute("INSERT OR REPLACE INTO cognitive_states VALUES ('state_1', 'CriticAgent', 'readiness', 'operational', 0.95, '2026-05-17 18:00:00')")
            cursor.execute("INSERT OR REPLACE INTO cognitive_states VALUES ('state_2', 'DreamAgent', 'dreamscape_mode', 'consolidation', 0.88, '2026-05-17 18:05:00')")
            cursor.execute("INSERT OR REPLACE INTO vault_metadata VALUES ('init_vault_doc', 'Sentience Layer System Diagnostics', 'system_report', '4.2 KB', 'encrypted', '2026-05-17 18:00:00')")
            
            self.conn.commit()
            self.is_initialized = True
            logger.info("Local PostgreSQL MCP database successfully initialized and seeded.")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize local PostgreSQL MCP: {e}")
            return False

    def list_tools(self) -> List[Dict[str, Any]]:
        """Expose PostgreSQL MCP Tools to the global registry"""
        return [
            {
                "name": "postgres_list_tables",
                "description": "Lists all available tables in the PostgreSQL database.",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "postgres_describe_table",
                "description": "Gets columns and schema information for a specific table.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "table_name": {
                            "type": "string",
                            "description": "Name of the table to describe."
                        }
                    },
                    "required": ["table_name"]
                }
            },
            {
                "name": "postgres_execute_query",
                "description": "Executes a SELECT SQL read query against the PostgreSQL database and returns the row records.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The SELECT SQL query string to run."
                        }
                    },
                    "required": ["query"]
                }
            }
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute the requested database tools against the SQLite relational engine"""
        if not self.is_initialized:
            self.initialize()

        cursor = self.conn.cursor()

        try:
            if name == "postgres_list_tables":
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                return {"status": "success", "tables": tables}

            elif name == "postgres_describe_table":
                table_name = arguments.get("table_name")
                # Whitelist table names to safeguard schema querying
                if table_name not in ["cognitive_states", "vault_metadata"]:
                    return {"status": "error", "error": f"Table '{table_name}' not found."}
                
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [{"name": row[1], "type": row[2]} for row in cursor.fetchall()]
                return {"status": "success", "table": table_name, "columns": columns}

            elif name == "postgres_execute_query":
                query = arguments.get("query", "")
                query_lower = query.strip().lower()
                
                # Enforce safe read-only SELECT queries
                if not query_lower.startswith("select"):
                    return {"status": "error", "error": "Only SELECT queries are allowed via the Postgres MCP interface."}
                
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                records = [dict(zip(columns, row)) for row in rows]
                return {"status": "success", "records": records}

            return {"status": "error", "error": f"Tool '{name}' is not supported by PostgresMcp."}

        except Exception as e:
            return {"status": "error", "error": str(e)}

def get_instance() -> PostgresMcp:
    return PostgresMcp()
