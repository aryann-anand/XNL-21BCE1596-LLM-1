import sys
import os

# Add the backend folder to the Python path so we can import app.py
sys.path.insert(0, os.path.join(os.getcwd(), "..", "backend"))

from mangum import Mangum
from app import app  # Assumes your FastAPI instance in backend/app.py is named "app"

# Wrap the FastAPI app with Mangum to adapt it for AWS Lambda
handler = Mangum(app)
