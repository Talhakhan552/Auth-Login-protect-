from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase_client import supabase

app = FastAPI(title="FlyRank Auth API")

class AuthBody(BaseModel):
    email: str = None
    password: str = None

@app.post("/auth/signup", status_code=201)
def signup(body: AuthBody):
    if not body.email or not body.password:
        raise HTTPException(status_code=400, detail="Email and password required")
    try:
        result = supabase.auth.sign_up({"email": body.email, "password": body.password})
        return result.user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login")
def login(body: AuthBody):
    if not body.email or not body.password:
        raise HTTPException(status_code=400, detail="Email and password required")
    try:
        result = supabase.auth.sign_in_with_password(
            {"email": body.email, "password": body.password}
        )
        return {
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token,
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid login credentials")