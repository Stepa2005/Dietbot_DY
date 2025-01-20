from sqlalchemy import String, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(25))
    sex: Mapped[str] = mapped_column(String(10))
    age: Mapped[int] = mapped_column()
    height: Mapped[int] = mapped_column()
    weight: Mapped[int] = mapped_column()
    ph_condition: Mapped[str] = mapped_column(String(200))
    ch_illnesses: Mapped[str] = mapped_column(String(100))
    goal: Mapped[str] = mapped_column(String(1000))
    is_registered: Mapped[bool] = mapped_column(default=False)


class BottomPFC(Base):
    __tablename__ = "PFC_bottoms"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    request: Mapped[str] = mapped_column(String(200))


class BottomDiet(Base):
    __tablename__ = "Diet_bottoms"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    request: Mapped[bool] = mapped_column(default=False)


class BottomTraining(Base):
    __tablename__ = "Training_bottoms"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    request: Mapped[bool] = mapped_column(default=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)