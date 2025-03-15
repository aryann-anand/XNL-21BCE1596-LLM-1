from fastapi import FastAPI
from mangum import Mangum  # To make FastAPI compatible with AWS Lambda (used by Vercel)

app = FastAPI()

# Import your existing app
from app import app as fastapi_app

handler = Mangum(fastapi_app)
