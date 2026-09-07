from fastapi import FastAPI
from app.api.resume import router as resume_router
from app.api.home import router as home_router

app = FastAPI()

app.include_router(home_router)
app.include_router(resume_router)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)
