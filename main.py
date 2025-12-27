from fastapi import FastAPI, Depends
from app.services.keycloak_service import keycloak_service
from app.core.security import get_current_user, require_realm_role



app = FastAPI()

@app.get('/')
async def root():
    return {'message: Hi World'}



@app.get('/jwks')
async def get_jwtk():
    return await keycloak_service.get_jwks()


@app.get('/service-token')
async def get_service_account_token():
    return await keycloak_service.get_service_account_token()



@app.post("/me")
async def me(user = Depends(get_current_user)):
    return user



@app.post("/role")
async def user_role(user=Depends(require_realm_role("admin"))):
    return user.get('realm_access')


@app.get('/healt')
async def health():
    return {"status": "ok"}