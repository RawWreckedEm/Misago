import pytest

from ...categories import CategoryTypes
from ...errors import CategoryNotFoundError
from ..validators import CategoryExistsValidator


@pytest.mark.asyncio
async def test_validator_returns_category_if_id_given_exists_in_db(category):
    validator = CategoryExistsValidator({})
    assert await validator(category.id) == category


@pytest.mark.asyncio
async def test_validator_raises_category_not_exists_error_if_category_not_exists(
    db,
):
    validator = CategoryExistsValidator({})
    with pytest.raises(CategoryNotFoundError):
        await validator(100)


@pytest.mark.asyncio
async def test_validator_returns_category_if_given_id_and_type_exists_in_db(category):
    validator = CategoryExistsValidator({}, CategoryTypes.THREADS)
    assert await validator(category.id) == category


@pytest.mark.asyncio
async def test_validator_raises_category_not_exists_error_for_wrong_category_type(
    category,
):
    validator = CategoryExistsValidator({}, CategoryTypes.PRIVATE_THREADS)
    with pytest.raises(CategoryNotFoundError):
        await validator(category.id)
