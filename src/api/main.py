import logging
import sys

from fastapi import FastAPI

from api.routers import crawl

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

app = FastAPI()
app.include_router(crawl.router)


@app.get("/heartbeat")
def home():
    return {"Hello": "World"}
