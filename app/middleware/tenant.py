from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        host = request.headers.get("host", "")
        subdomain = None

        # Extract subdomain only if it's in the format subdomain.domain.tld
        if host and "." in host:
            parts = host.split(".")
            if len(parts) > 2:
                subdomain = parts[0]  # e.g., sunshine from sunshine.skolanova.org

        request.state.tenant_slug = subdomain

        # Optional: handle unknown or missing subdomain
        if not subdomain:
            return Response("Tenant subdomain missing or invalid", status_code=400)

        response = await call_next(request)
        return response
