from datetime import timedelta

import pytest

from ...utils import timezone
from ..token import (
    create_user_token,
    decode_jwt_token,
    encode_jwt_token,
    get_jwt_exp,
    get_jwt_secret,
    get_user_from_token,
)

SECRET = "secret"
PAYLOAD = {"test": "ok!"}


def test_jwt_token_can_be_encoded_and_decoded_back():
    token = encode_jwt_token(SECRET, PAYLOAD)
    assert decode_jwt_token(SECRET, token) == PAYLOAD


def test_jwt_token_is_not_decoded_if_secret_is_incorrect():
    token = encode_jwt_token(SECRET, PAYLOAD)
    assert decode_jwt_token("incorrect", token) is None


def test_jwt_token_is_not_decoded_if_payload_is_incorrect():
    assert decode_jwt_token(SECRET, "incorrect") is None


def test_util_creates_jwt_exp_date_using_context():
    exp = get_jwt_exp({"settings": {"jwt_exp": 60}})
    assert exp > timezone.now() + timedelta(seconds=59)
    assert exp < timezone.now() + timedelta(seconds=61)


def test_util_extracts_jwt_secret_from_context():
    assert get_jwt_secret({"settings": {"jwt_secret": SECRET}}) == SECRET


@pytest.mark.asyncio
async def test_user_token_can_be_created(context, user):
    token = await create_user_token(context, user)
    secret = get_jwt_secret(context)
    payload = decode_jwt_token(secret, token)
    assert payload["user"] == user.id


@pytest.mark.asyncio
async def test_user_can_be_obtained_from_token(context, user):
    token = await create_user_token(context, user)
    assert await get_user_from_token(context, token) == user


@pytest.mark.asyncio
async def test_no_user_is_returned_for_invalid_token(context):
    user = await get_user_from_token(context, "invalid")
    assert user is None


@pytest.mark.asyncio
async def test_deleted_user_is_not_obtained_from_token(context, user):
    token = await create_user_token(context, user)
    await user.delete()
    assert await get_user_from_token(context, token) is None
