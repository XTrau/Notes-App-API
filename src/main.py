from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import drop_tables, create_tables
from auth.router import router as auth_router
from notes.router import router as notes_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(notes_router)

allow_headers = [
    "Content-Type",
    "Authorization",
    "X-Requested-With",
    "Accept",
    "Origin",
    "User-Agent",
    "DNT",
    "Cache-Control",
    "X-Mx-ReqToken",
    "Keep-Alive",
    "X-Requested-With",
    "If-Modified-Since",
    "X-CSRF-Token"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=allow_headers
)


@app.get("/")
async def root():
    try:
        await create_tables()
    except Exception as e:
        return {"error": "Failed connect to database"}
    return {"Status": "Server Working!"}


@app.post("/reset_db")
async def reset_database():
    await drop_tables()
    await create_tables()
    return {"message": "Database reseted!"}
