# Testing

## Setup

```bash
# Install dev dependencies
uv sync --extra dev

# Create test database
docker exec -it rag-postgres psql -U postgres -c "CREATE DATABASE rag_demo_test;"
```

## Running Tests

```bash
pytest                                    # All tests
pytest -v                                 # Verbose
pytest tests/test_health.py              # Specific file
pytest tests/test_health.py::test_health_check  # Specific test
pytest --cov=src --cov-report=html       # With coverage
```

## Test Structure

```
tests/
├── conftest.py      # Fixtures
├── test_app.py      # Configuration tests
└── test_health.py   # API tests
```

## Fixtures

| Fixture | Scope | Description |
|---------|-------|-------------|
| `test_settings` | session | Settings with test database |
| `test_engine` | session | Engine with auto table creation/deletion |
| `db_session` | function | Session with rollback after each test |
| `client` | function | AsyncClient for HTTP requests |

## Writing Tests

### Database Test

```python
# tests/test_items.py
from sqlalchemy import select
from src.models.item import Item


async def test_create_item(db_session):
    item = Item(name="Test")
    db_session.add(item)
    await db_session.flush()

    result = await db_session.execute(select(Item))
    items = result.scalars().all()
    assert len(items) == 1
    assert items[0].name == "Test"


async def test_item_timestamps(db_session):
    item = Item(name="Test")
    db_session.add(item)
    await db_session.flush()

    assert item.created_at is not None
    assert item.updated_at is not None
```

### API Test

```python
# tests/test_api.py
from httpx import AsyncClient


async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_get_items(client: AsyncClient):
    response = await client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_create_item(client: AsyncClient):
    response = await client.post("/items/", json={"name": "Test"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test"
```

### Test with Mocking

```python
from unittest.mock import AsyncMock, patch


async def test_external_service(client: AsyncClient):
    with patch("src.services.external.fetch_data", new_callable=AsyncMock) as mock:
        mock.return_value = {"data": "mocked"}
        response = await client.get("/external/")
        assert response.status_code == 200
        mock.assert_called_once()
```

## Configuration

Test settings in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

Environment variable for test database:

```bash
TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/rag_demo_test
```
