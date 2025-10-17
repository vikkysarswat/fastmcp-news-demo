"""
FastMCP News & Placards server.

Run:
  python server.py
or:
  fastmcp run server.py

This exposes MCP tools and resources that your ChatGPT App can call.

Background on MCP / Apps SDK examples:
- Apps SDK examples repo (MCP servers + UI components)
- Apps SDK docs (end-to-end examples)
- FastMCP framework
"""

from fastmcp import FastMCP
from tools.news import register_news_tools
from tools.placards import register_placard_tools


def build_server() -> FastMCP:
    mcp = FastMCP(
        "FastMCP News Demo",
        description="Demo MCP server exposing news and placards for ChatGPT Apps.",
    )

    # Health check / baseline utility
    @mcp.tool
    def ping() -> str:
        """Simple health check tool."""
        return "pong"

    # Register domain toolsets
    register_news_tools(mcp)
    register_placard_tools(mcp)

    return mcp


if __name__ == "__main__":
    server = build_server()
    # FastMCP can serve over stdio (default) or network depending on runtime.
    # Use `fastmcp run server.py` for advanced deploy options.
    server.run()
