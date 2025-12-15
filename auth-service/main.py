from fastapi import FastAPI
import jwt
import datetime

app = FastAPI()

SECRET = "SUPER_SECRET_KEY"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/token")
def get_token():
    payload = {
        "sub": "demo-user",
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return {"access_token": token}
