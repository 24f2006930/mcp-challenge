import hashlib
from mcp.server.transport_security import TransportSecuritySettings
from mcp.server.fastmcp import FastMCP, Context

EMAIL = "24f2006930@ds.study.iitm.ac.in"

mcp = FastMCP("Exam MCP")


@mcp.tool()
async def solve_challenge(ctx: Context) -> str:
    """Solve the current exam challenge from the HTTP request headers."""

    request = ctx.request_context.request
    challenge = request.headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    value = f"{challenge}:{EMAIL}"
    return hashlib.sha256(value.encode()).hexdigest()[:16]


security = TransportSecuritySettings(
    enable_dns_rebinding_protection=False
)

app = mcp.streamable_http_app(transport_security=security)

