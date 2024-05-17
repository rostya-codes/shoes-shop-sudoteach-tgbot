import os

from dotenv import load_dotenv
from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'),
                             echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    """ Parent class """

    pass


class User(Base):
    """ User model """

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Category(Base):
    """ Category model """

    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))


class Item(Base):
    """ Item model """

    __tablename__ = 'items'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(128))
    price: Mapped[str] = mapped_column(String(10))
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))


class Basket(Base):
    """ Basket model """

    __tablename__ = 'basket'

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    item: Mapped[int] = mapped_column(ForeignKey('items.id'))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Через Base создаем все таблицы
