import httpx
from fastapi import HTTPException
from app.core.config import settings
from app.models.auth_models import RegisterBody, LoginBody



class KeycloakService:

    def __init__ (self) -> None:
        self.issuer = f"{settings.keycloak_base_url}/realms/{settings.keycloak_realm}"
        self.token_url = f"{self.issuer}/protocol/openid-connect/token"
        self.users_url = f"{settings.keycloak_base_url}/admin/realms/{settings.keycloak_realm}/users"
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
        

    async def get_service_account_token(self) -> str:
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
            self._service_token_cache=token['access_token']
            return self._service_token_cache


    async def register_user(self, body: RegisterBody) -> str:
        service_token = await self.get_service_account_token()

        headers = {
            "Authorization": f"Bearer {service_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "username": body.username,
            "email": body.email,
            "firstName": body.first_name,
            "lastName": body.last_name,
            "enabled": True,
            "emailVerified": False,
            "credentials": [
                {
                    "type": "password",
                    "value": body.password,
                    "temporary": False,
                }
            ],
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.users_url, data=payload, headers=headers, timeout=10)

        if response.status_code != 201:
            raise HTTPException(response.status_code, f"Keycloak create user failed: {response.text}")

        location = response.headers.get("Location", "")
        user_id= location.rsplit("/", 1)[-1]
        return user_id


    async def login_user(self, body: LoginBody) -> dict[str, str]:
        data = {
            "grant_type": "password",
            "client_id": settings.keycloak_client_id,
            "client_secret": settings.keycloak_client_secret,
            "username": body.email,
            "password": body.password,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.token_url, data=data, timeout=10)

        if response.status_code != 200:
            raise HTTPException(status_code=401, detail=f"Login failed: {response.text}")

        json_response = response.json()

        return {
            "access_token": json_response["access_token"],
            "refresh_token": json_response.get("refresh_token"),
        }


    def clear_service_token_cache(self) -> None:
        self._service_token_cache = None
   


keycloak_service = KeycloakService()





