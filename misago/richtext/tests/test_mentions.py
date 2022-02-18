from unittest.mock import ANY

import pytest

from ..parser import parse_markup


@pytest.mark.asyncio
async def test_quote_author_is_included_in_mentions(context, user):
    result, metadata = await parse_markup(context, f"[quote={user.name}]Text[/quote]")

    assert result == [
        {
            "id": ANY,
            "type": "quote",
            "author": {
                "id": user.id,
                "name": user.name,
                "slug": user.slug,
            },
            "post": None,
            "children": [{"id": ANY, "type": "p", "text": "Text"}],
        }
    ]
    assert user.slug in metadata["mentions"]


@pytest.mark.asyncio
async def test_mentioned_user_is_included_in_mentions(context, user):
    result, metadata = await parse_markup(context, f"@{user.name}, wsup?")

    assert result == [
        {
            "id": ANY,
            "type": "p",
            "text": (
                f'<a href="/u/{user.slug}/{user.id}/" data-quote="@{user.name}">'
                f"@{user.name}</a>, wsup?"
            ),
        }
    ]
    assert user.slug in metadata["mentions"]
