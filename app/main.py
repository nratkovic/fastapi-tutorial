from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import auth
from .routers import post
from .routers import user
from .routers import vote

# statement to create all tables not needed if using Alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.project_name, version=settings.project_version)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI project!!!"}
