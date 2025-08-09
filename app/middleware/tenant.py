# app/middleware/tenant.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.core.database import get_tenant_by_slug, SessionLocal


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tenant_slug = None

        # 1️⃣ Try subdomain (prod case)
        host = request.headers.get("host", "")
        if "." in host:
            subdomain = host.split(".")[0]
            if subdomain not in ("www", "localhost", "127"):
                tenant_slug = subdomain

        # 2️⃣ Try header (dev case)
        if not tenant_slug:
            tenant_slug = request.headers.get("X-Tenant")

        # 3️⃣ Try query param (fallback)
        if not tenant_slug:
            tenant_slug = request.query_params.get("tenant_slug")

        if not tenant_slug:
            return Response(
                content='{"detail": "Tenant not found"}',
                media_type="application/json",
                status_code=404,
            )

        # ✅ Use DB session
        db = SessionLocal()
        try:
            tenant = get_tenant_by_slug(db, tenant_slug)
        finally:
            db.close()

        if not tenant:
            return Response(
                content='{"detail": "Tenant not found"}',
                media_type="application/json",
                status_code=404,
            )

        request.state.tenant = tenant
        return await call_next(request)


# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.requests import Request
# from starlette.responses import Response, JSONResponse

# from app.core.database import get_tenant_scoped_session
# from app.models.tenant import Tenant


# class TenantMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         host = request.headers.get("host", "")
#         subdomain = None

#         if host and "." in host:
#             parts = host.split(".")
#             if len(parts) > 2:
#                 subdomain = parts[0]

#         if not subdomain:
#             subdomain = request.headers.get("X-Tenant")

#         if not subdomain:
#             return JSONResponse(
#                 {"detail": "Tenant subdomain missing or invalid"}, status_code=400
#             )

#         # Open raw session to query tenant
#         raw_db = get_tenant_scoped_session()
#         tenant = raw_db.query(Tenant).filter(Tenant.slug == subdomain).first()
#         raw_db.close()

#         if not tenant:
#             return JSONResponse({"detail": "Tenant not found"}, status_code=404)

#         request.state.tenant = tenant

#         # Create tenant-scoped session for request
#         request.state.db = get_tenant_scoped_session(tenant_id=tenant.id)

#         try:
#             response = await call_next(request)
#         finally:
#             request.state.db.close()

#         return response
