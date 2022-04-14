from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

app=FastAPI()

@app.get("/")
async def index():
    return {"Message":"Hello world"}

register_tortoise(
                  app,
                  db_url="sqlite://database.sqlite3",
                  modules={"models" : ["models"]},
                  add_exception_handlers=True,
                  generate_schemas=True
                  )

