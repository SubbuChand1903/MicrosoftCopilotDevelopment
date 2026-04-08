from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.ui_router import router
from routes.invoke_router import router as invoke_router

app = FastAPI(title="AdaptiveOps API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)
app.include_router(invoke_router)

@app.get("/")
def root():
    return {"status": "running"}