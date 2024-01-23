import datetime

from fastapi import FastAPI

from nordic_realm.utils.default_base_model import DefaultBaseModel

app = FastAPI()


class MyModel(DefaultBaseModel):
    my_date: datetime.date
    my_datetime: datetime.datetime


@app.get(path="/auth/test")
def root():
    my_model = MyModel(
        my_date=datetime.datetime.utcnow().date(),
        my_datetime=datetime.datetime.utcnow()
    )

    return my_model.model_dump()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
