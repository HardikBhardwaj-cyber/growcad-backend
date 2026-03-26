from fastapi import FastAPI
from app.middleware.tenant import TenantMiddleware
from app.api.auth import router as auth_router
from app.api.test_secure import router as test_router
from app.api.student import router as student_router
from app.api.batch import router as batch_router
from app.db.base import Base
from app.db.session import engine

# 🔥 CREATE TABLES (TEMP FOR NOW)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(TenantMiddleware)

app.include_router(auth_router)
app.include_router(test_router)
app.include_router(student_router)
app.include_router(batch_router)


@app.get("/")
def root():
    return {"message": "Growcad API running"}