from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import engine

# ✅ IMPORT THIS
from app.api.upload import router as upload_router

app = FastAPI()

# ✅ ADD THIS
app.include_router(upload_router, prefix="/api")

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/db-test")
def test_db():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"db": "connected"}
    except Exception as e:
        return {"error": str(e)}