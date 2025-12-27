import httpx
from fastapi import HTTPException
from app.core.config import settings



class KeycloakService:

    def __init__ (self) -> None:
        self.issuer = f"{settings.keycloak_base_url}/realms/{settings.keycloak_realm}"
        self.token_url = f"{self.issuer}/protocol/openid-connect/token"
        self.admin_users_url = f"{settings.keycloak_base_url}/admin/realms/{settings.keycloak_realm}/users"
        self.jwks_url = f"{self.issuer}/protocol/openid-connect/certs"
        self._service_token_cache: str | None = None
        self._jwks_cache: dict | None = None


    async def get_jwks(self) -> dict:
        if self._jwks_cache:
            return self._jwks_cache
        
        async with httpx.AsyncClient() as client:
            response= await client.get(self.jwks_url, timeout=10)
            response.raise_for_status()
            print(response.json())
            self._jwks_cache = response.json()
            return self._jwks_cache
        


    async def get_service_account_token(self) -> None:
        if self._service_token_cache:
            return self._service_token_cache
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': settings.keycloak_client_id,
            'client_secret': settings.keycloak_client_secret
        }
        
        async with httpx.AsyncClient() as client:
            response= await client.post(self.token_url, data=data, timeout=10)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=f"Keycloak admin token failed: {response.text}"
                )
            
            token = response.json()
            self._admin_token_cache=token['access_token']
            return self._admin_token_cache
        
    def clear_service_token_cache(self) -> None:
        self._service_token_cache = None
   

keycloak_service = KeycloakService()





