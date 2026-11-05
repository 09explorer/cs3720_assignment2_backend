from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
# from datetime import datetime

# --- MongoDB connection ---
uri = "mongodb+srv://tennisboy421_db_user:fZdpfWqM9NtvuvQa@cluster0.qx92fh5.mongodb.net/"

client = MongoClient(uri)
db = client["cs3720db"]               # Database name
collection = db["robots"]             # Collection name (not robots.json, just robots)

# --- FastAPI app setup ---
app = FastAPI()

# Optional: enable CORS if you’ll connect from React/React Native
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # or specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Minimal Pydantic model ---
class Robot(BaseModel):
    name: str
    price: float
    description: str
    imageUrl: str

# --- Root endpoint ---
@app.get("/hello")
def read_root():
    return {"message": "Hello from FastAPI + MongoDB Atlas backend!"}


# --- Get all robots ---
@app.get("/robots")
def get_robots():
    robots = list(collection.find())      # Retrieve all documents
    for r in robots:
        r["_id"] = str(r["_id"])          # Convert ObjectId to string
    return robots

@app.post("/robots", status_code=status.HTTP_201_CREATED)
def add_robot(robot: Robot):
    collection.insert_one(robot.dict())
    return {"message": "Robot added successfully"}

