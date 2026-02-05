# Development Guide

## Adding a Model

Create model file:

```python
# src/models/item.py
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin


class Item(Base, TimestampMixin):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str | None]
```

Register in `src/models/__init__.py`:

```python
from src.models.base import Base
from src.models.item import Item

__all__ = ["Base", "Item"]
```

Create and apply migration:

```bash
alembic revision --autogenerate -m "Add items table"
alembic upgrade head
```

## Adding a Route

Create router file:

```python
# src/api/routes/items.py
from fastapi import APIRouter
from sqlalchemy import select

from src.api.deps import DbSession
from src.models.item import Item

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/")
async def get_items(db: DbSession):
    result = await db.execute(select(Item))
    return result.scalars().all()


@router.get("/{item_id}")
async def get_item(item_id: int, db: DbSession):
    result = await db.execute(select(Item).where(Item.id == item_id))
    return result.scalar_one_or_none()


@router.post("/")
async def create_item(name: str, db: DbSession):
    item = Item(name=name)
    db.add(item)
    await db.flush()
    return item
```

Include in `src/api/routes/__init__.py`:

```python
from fastapi import APIRouter

from src.api.routes.items import router as items_router

router = APIRouter()
router.include_router(items_router)
```

## Adding a Service

Create service file with business logic:

```python
# src/services/items.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.item import Item


async def get_items(db: AsyncSession) -> list[Item]:
    result = await db.execute(select(Item))
    return list(result.scalars().all())


async def get_item_by_id(db: AsyncSession, item_id: int) -> Item | None:
    result = await db.execute(select(Item).where(Item.id == item_id))
    return result.scalar_one_or_none()


async def create_item(db: AsyncSession, name: str, description: str | None = None) -> Item:
    item = Item(name=name, description=description)
    db.add(item)
    await db.flush()
    return item
```

Use in routes:

```python
from src.services import items as items_service

@router.get("/")
async def get_items(db: DbSession):
    return await items_service.get_items(db)
```

## Pydantic Schemas

Create schemas for request/response validation:

```python
# src/schemas/items.py
from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    description: str | None = None


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None

    model_config = {"from_attributes": True}
```

Use in routes:

```python
from src.schemas.items import ItemCreate, ItemResponse

@router.post("/", response_model=ItemResponse)
async def create_item(data: ItemCreate, db: DbSession):
    return await items_service.create_item(db, data.name, data.description)
```
