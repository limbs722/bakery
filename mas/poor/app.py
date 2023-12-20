from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware


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

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:appl', host='0.0.0.0', port=8000, reload=True)