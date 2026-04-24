from fastapi import FastAPI
from .core.database import engine, Base
from .routes.url_routes import router
from .models import url_model
from .models import user_model
from .routes.user_routes import router as user_router
from .models import check_result_model
from fastapi.middleware.cors import CORSMiddleware
from .services.scheduler import start_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI()

start_scheduler()

app.include_router(router)
app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Server running"}