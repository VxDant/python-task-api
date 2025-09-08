from fastapi import HTTPException, Security, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
import os

security = HTTPBearer()

# API Keys for different purposes
API_KEYS = {
    "demo": os.getenv("DEMO_API_KEY", "demo-key-for-swagger-ui"),
    "ci_cd": os.getenv("CICD_API_KEY", "cicd-pipeline-key"),
    "admin": os.getenv("ADMIN_API_KEY", "admin-super-key")
}

# Track API usage (simple in-memory for demo)
api_usage = {}


async def verify_api_key(request: Request, credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify API key for general access"""
    api_key = credentials.credentials
    client_ip = request.client.host

    # Find which key type was used
    key_type = None
    for key_name, key_value in API_KEYS.items():
        if api_key == key_value:
            key_type = key_name
            break

    if not key_type:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    # Track usage for monitoring
    usage_key = f"{client_ip}:{key_type}"
    current_time = datetime.now()

    if usage_key in api_usage:
        api_usage[usage_key]["count"] += 1
        api_usage[usage_key]["last_used"] = current_time
    else:
        api_usage[usage_key] = {
            "count": 1,
            "first_used": current_time,
            "last_used": current_time
        }

    # Add usage info to request state
    request.state.api_key_type = key_type
    request.state.client_ip = client_ip

    return {"key_type": key_type, "authenticated": True}


# THIS WAS MISSING - Admin key verification
async def verify_admin_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify admin API key for administrative functions"""
    if credentials.credentials != API_KEYS["admin"]:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return {"admin": True, "authenticated": True}


# Optional: Simple user info (if you don't need to full JWT auth)
async def get_current_user(request: Request, api_info: dict = Depends(verify_api_key)):
    """Get current 'user' info based on API key (simplified)"""
    return {
        "user_type": api_info["key_type"],
        "ip_address": request.client.host,
        "authenticated": True
    }
