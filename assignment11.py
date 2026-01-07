from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "MYSECRET123"
REFRESH_SECRET_KEY = "MYREFRESHSECRET123"  # separate secret for refresh tokens
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

users = {
    "abcd": {"username": "abcd", "password": "1234"},
    "klmno": {"username": "klmno", "password": "abcd"}
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(username: str):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, REFRESH_SECRET_KEY, algorithm=ALGORITHM)


@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    username = form.username
    password = form.password

    if username not in users or users[username]["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(username)
    refresh_token = create_refresh_token(username)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def verify_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.post("/refresh")
def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["sub"]
        new_access_token = create_access_token(username)
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


@app.get("/profile")
def profile(username: str = Depends(verify_access_token)):
    return {"message": "Welcome!", "user": username}
