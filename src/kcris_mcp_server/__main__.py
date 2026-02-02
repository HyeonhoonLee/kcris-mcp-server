"""uvx/uv run 진입점: K-CRIS MCP 서버를 stdio 전송으로 실행합니다."""

from __future__ import annotations

from kcris_mcp_server.server import mcp


def main() -> None:
    """MCP 서버를 stdio 전송으로 실행."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
