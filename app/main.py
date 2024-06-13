from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from tenacity import retry, stop_after_attempt, wait_exponential
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# Create all the tables
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Path Operation / Route
@app.get("/")
async def root():
    return {"message": "Test FastAPI"}
