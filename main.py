from fastapi import FastAPI

from misc.model import create_admin
from models import Base, engine
from routes import init_app_routes


app = FastAPI(title="MyEXAM", version="0.1.0")

init_app_routes(app)

Base.metadata.create_all(bind=engine)
create_admin()
