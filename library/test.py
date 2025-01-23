import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_operation():
    async def async_task(value):
        await asyncio.sleep(1)
        return value

    result = await async_task(42)
    assert result == 42

@pytest.mark.asyncio
async def test_exception_handling():
    async def async_task(value):
        if value < 0:
            raise ValueError("Negative value")
        return value

    try:
        await async_task(-5)
    except ValueError as e:
        assert str(e) == "Negative value"
    else:
        pytest.fail("Exception not raised")