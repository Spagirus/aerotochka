import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.customer_api import router as customer_router
from src.exceptions import NotFound404Error, Conflict409Error

app = FastAPI()

app.include_router(customer_router)


@app.exception_handlers(NotFound404Error)
def error_404(request: Request, err: NotFound404Error):
    return JSONResponse(
        status_code=404,
        content=
        {
            "detail": {
                "code": err.code,
                "message": err.message
            }
        }
    )


@app.exception_handlers(Conflict409Error)
def error_400(request: Request, err: NotFound404Error):
    return JSONResponse(
        status_code=404,
        content=
        {
            "detail": {
                "code": err.code,
                "message": err.message
            }
        }
    )


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
