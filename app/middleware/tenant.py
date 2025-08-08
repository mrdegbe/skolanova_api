from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from app.core.database import get_tenant_scoped_session
from app.models.tenant import Tenant


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        host = request.headers.get("host", "")
        subdomain = None

        if host and "." in host:
            parts = host.split(".")
            if len(parts) > 2:
                subdomain = parts[0]

        if not subdomain:
            return JSONResponse(
                {"detail": "Tenant subdomain missing or invalid"}, status_code=400
            )

        # Open raw session to query tenant
        raw_db = get_tenant_scoped_session()
        tenant = raw_db.query(Tenant).filter(Tenant.slug == subdomain).first()
        raw_db.close()

        if not tenant:
            return JSONResponse({"detail": "Tenant not found"}, status_code=404)

        request.state.tenant = tenant

        # Create tenant-scoped session for request
        request.state.db = get_tenant_scoped_session(tenant_id=tenant.id)

        try:
            response = await call_next(request)
        finally:
            request.state.db.close()

        return response
