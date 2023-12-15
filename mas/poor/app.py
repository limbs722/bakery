from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from bakery.app.poor.service import Service

service = Service()

appl = FastAPI()
appl.add_middleware(SessionMiddleware, secret_key="secret-key")

origins = [ "*" ]

appl.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

"""
    API list
    - sign in, sign up
    - get list
    - write trial
    - write comment
"""

@appl.post("/user/signup")
async def enroll_user(data):
    try:
        service.signup(data.email)
        return dict(status='success', email=data.email)

    except Exception as e:
        return HTTPException(status_code=500, detail=(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:appl', host='0.0.0.0', port=8000, reload=True)