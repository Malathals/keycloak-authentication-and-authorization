from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from jose import jwt
from app.services.keycloak_service import keycloak_service
from app.core.config import settings

bearer = HTTPBearer()
ISSUER = f"{settings.keycloak_base_url}/realms/{settings.keycloak_realm}"


async def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    token= creds.credentials
    print("creds.credentials", creds.credentials)

    jwks = await keycloak_service.get_jwks()

    try:
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")


        key = next((k for k in jwks['keys'] if k['kid'] == kid), None)
        if not key:
            raise HTTPException(status_code=401, detail="Invalid token key id")
        
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=settings.keycloak_audience,
            issuer=ISSUER,
        )
        return payload
    
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")



def require_realm_role(role: str):
    def _checker(user: dict = Depends(get_current_user)):
        print(user)
        roles= (user.get("realm_access") or {}).get('roles') or []
        print("roles", roles)

        if role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden") 
        return user 
    return _checker

