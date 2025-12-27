from fastapi import FastAPI, Depends
from app.services.keycloak_service import keycloak_service
from app.core.security import get_current_user
from app.models.auth_models import RegisterBody, LoginBody

app = FastAPI()

@app.get('/')
async def root():
    return {'message: Hello World'}

@app.post("/me")
async def me(user = Depends(get_current_user)):
    return user

@app.post("/register")
async def register(body: RegisterBody):
    user_id = await keycloak_service.register_user(body)
    return {"user_id": user_id}


@app.post("/login")
async def login(body: LoginBody):
    return await keycloak_service.login_user(body)


@app.get('/health')
async def health():
    return {"status": "ok"}