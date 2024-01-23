from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

app = FastAPI()


class MyException(Exception):
    pass


@app.get(path="/auth/test")
def root():
    raise MyException()


def my_exception_handler(request: Request, exception: Exception):
    return JSONResponse({}, 401)


app.add_exception_handler(MyException, my_exception_handler)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
