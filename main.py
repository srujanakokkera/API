from fastapi import FastAPI
from database import engine
from models import Base
from routes import router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.requests import Request

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [{"field": err["loc"][-1], "message": err["msg"]} for err in exc.errors()]
    return JSONResponse(status_code=422, content={"errors": errors})

app.include_router(router)
