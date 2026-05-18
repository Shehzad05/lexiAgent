"""
Entry point — run with:  uvicorn main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.routes import router
from config import settings

app = FastAPI(
    title="LexiAgent API",
    description="Autonomous Legal Contract Analyzer",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes PEHLE register karo
app.include_router(router, prefix="/api")

# Static files (CSS, JS etc) serve karo
app.mount("/static", StaticFiles(directory="ui"), name="static")

# Root pe index.html serve karo
@app.get("/")
async def serve_ui():
    return FileResponse("ui/index.html")

# Koi bhi unknown route pe bhi index.html do
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    return FileResponse("ui/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)