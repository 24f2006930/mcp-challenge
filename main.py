import hashlib

from mcp.server.fastmcp import FastMCP, Context
from mcp.server.transport_security import TransportSecuritySettings

EMAIL = "24f2006930@ds.study.iitm.ac.in"

mcp = FastMCP(
    "Exam MCP",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False
    ),
)


@mcp.tool()
async def solve_challenge(ctx: Context) -> str:
    """Solve the current exam challenge from the HTTP request headers."""
    request = ctx.request_context.request
    challenge = request.headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    value = f"{challenge}:{EMAIL}"
    return hashlib.sha256(value.encode()).hexdigest()[:16]


app = mcp.streamable_http_app()
