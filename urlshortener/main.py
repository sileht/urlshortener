import logging
import os
import uuid

import databases
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl
import sqlalchemy
import tenacity


logging.basicConfig()
LOG = logging.getLogger(__name__)

DATABASE_TEST_PORT = os.getenv("DATABASE_TEST_PORT", 12345)
DATABASE_URL = os.getenv("QOVERY_DATABASE_MY_POSTGRESSQL_CONNECTION_URI")
if not DATABASE_URL:
    DATABASE_URL = os.getenv(
        "DATABASE_URL", f"postgresql://test:test@127.0.0.1:{DATABASE_TEST_PORT}/test"
    )

app = FastAPI()

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


Urls = sqlalchemy.Table(
    "urls",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("urlhash", sqlalchemy.String, unique=True),
    sqlalchemy.Column("url", sqlalchemy.String),
)


class UrlEncoderBodyIn(BaseModel):
    url: HttpUrl = Field(..., title="The url to convert in a shorter one")


class UrlEncoderBody(UrlEncoderBodyIn):
    urlhash: str = Field(..., title="The hash to retrieve the url")


@tenacity.retry(
    stop=tenacity.stop_after_attempt(60 * 5), wait=tenacity.wait_fixed(1),
)
def wait_for_database(connection):
    try:
        connection.execute("SELECT 1")
    except Exception as e:
        LOG.warning("fail to connect to the database, retrying: %s", e)
        raise


# Create DB on startup
engine = sqlalchemy.create_engine(DATABASE_URL)
wait_for_database(engine)
metadata.create_all(engine)
engine.dispose()


@app.on_event("startup")
async def startup():

    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/{urlhash}")
async def decode(urlhash: str):
    query = Urls.select().where(Urls.c.urlhash == urlhash)
    row = await database.fetch_one(query)
    if row:
        return RedirectResponse(url=row["url"])
    else:
        raise HTTPException(status_code=404, detail="urlhash not foun")


@app.post("/encode", response_model=UrlEncoderBody)
async def encode(body: UrlEncoderBodyIn):
    # NOTE(sileht): Create a hash unique enough to avoid collision
    # then retry if it fail
    urlhash = uuid.uuid4().hex[0:7]
    query = Urls.insert().values(urlhash=urlhash, url=body.url)
    last_id = await database.execute(query)
    query = Urls.select().where(Urls.c.id == last_id)
    return await database.fetch_one(query)
