from datetime import datetime, timedelta
from typing import Any, Awaitable, Dict, Optional

import jwt
from jwt.exceptions import InvalidTokenError

from ..context import Context
from ..users.models import User
from ..utils import timezone
from .hooks import (
    create_user_token_hook,
    create_user_token_payload_hook,
    get_auth_user_hook,
    get_user_from_token_payload_hook,
)
from .user import get_user

JWT_ALGORITHM = "HS256"


def create_user_token(
    context: Context, user: User, in_admin: bool = False
) -> Awaitable[str]:
    return create_user_token_hook.call_action(
        create_user_token_action, context, user, in_admin
    )


async def create_user_token_action(
    context: Context, user: User, in_admin: bool = False
) -> str:
    secret = get_jwt_secret(context)
    payload = await create_user_token_payload_hook.call_action(
        create_user_token_payload, context, user, in_admin
    )
    return encode_jwt_token(secret, payload)


async def create_user_token_payload(
    context: Context, user: User, in_admin: bool = False
) -> Dict[str, Any]:
    return {"exp": get_jwt_exp(context), "user": user.id}


def get_jwt_exp(context: Context) -> datetime:
    return timezone.now() + timedelta(seconds=context["settings"]["jwt_exp"])


async def get_user_from_token(
    context: Context, token: str, in_admin: bool = False
) -> Optional[User]:
    secret = get_jwt_secret(context)
    token_payload = decode_jwt_token(secret, token)
    if not token_payload:
        return None

    return await get_user_from_token_payload_hook.call_action(
        get_user_from_token_payload, context, token_payload, in_admin
    )


async def get_user_from_token_payload(
    context: Context, token_payload: Dict[str, Any], in_admin: bool = False
) -> Optional[User]:
    if token_payload.get("user"):
        return await get_auth_user_hook.call_action(
            get_user, context, token_payload["user"], in_admin
        )
    return None


def get_jwt_secret(context: Context) -> str:
    return context["settings"]["jwt_secret"]


def encode_jwt_token(secret: str, payload: Dict[str, Any]) -> str:
    return jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)


def decode_jwt_token(secret: str, token: str) -> Optional[Dict[str, Any]]:
    try:
        return jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
    except InvalidTokenError:
        return None
