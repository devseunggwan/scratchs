import os
from datetime import datetime

from databases import Database
from sqlalchemy import Column, Integer, String, create_engine, Table, MetaData
from dotenv import load_dotenv
from pytz import timezone as tz

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://hello_fastapi:hello_fastapi@localhost/hello_fastapi_dev")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("completed", String(8), default="False"),
    Column("created_date", String(50), default=datetime.now(tz("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S"))
)

database = Database(DATABASE_URL)
