# FastAPI + Keycloak Simple Auth

This project implements a basic authentication system using **FastAPI** and **Keycloak**.

Supports:
- Register user in Keycloak
- Login
- Protected route using JWT
- Swagger UI for testing

---

## Requirements

- Python 3.9+
- Keycloak running

---

## Install & Run

```bash
pip install fastapi uvicorn httpx pydantic "python-jose[cryptography]"
uvicorn main:app --reload
