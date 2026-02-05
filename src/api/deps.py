from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db

DbSession = Annotated[AsyncSession, Depends(get_db)]


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    from src.database import get_db

    async for session in get_db():
        yield session
