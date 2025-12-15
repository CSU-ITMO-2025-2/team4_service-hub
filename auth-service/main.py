from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import datetime
import os

app = FastAPI()

SECRET = os.getenv("JWT_SECRET", "dev-secret")
ALGORITHM = "HS256"

security = HTTPBearer()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/token")
def get_token():
    payload = {
        "sub": "demo-user",
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return {"access_token": token}


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


@app.get("/protected")
def protected(payload: dict = Depends(verify_token)):
    return {
        "message": "Access granted",
        "user": payload["sub"]
    }
