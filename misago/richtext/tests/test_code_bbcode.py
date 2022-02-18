from unittest.mock import ANY

import pytest

from ..parser import parse_markup


@pytest.mark.asyncio
async def test_code_bbcode_is_supported(context):
    result, _ = await parse_markup(context, "[code]Hello **world**![/code]")
    assert result == [
        {"id": ANY, "type": "code", "syntax": None, "text": "Hello **world**!"}
    ]


@pytest.mark.asyncio
async def test_multiline_code_bbcode_is_supported(context):
    result, _ = await parse_markup(context, "[code]\nHello **world**!\n[/code]")
    assert result == [
        {"id": ANY, "type": "code", "syntax": None, "text": "Hello **world**!"}
    ]


@pytest.mark.asyncio
async def test_code_bbcode_is_parsed_before_indented_code(context):
    result, _ = await parse_markup(context, "[code]\n    Hello **world**!\n[/code]")
    assert result == [
        {"id": ANY, "type": "code", "syntax": None, "text": "Hello **world**!"}
    ]


@pytest.mark.asyncio
async def test_code_bbcode_with_syntax_is_supported(context):
    result, _ = await parse_markup(context, "[code=python]Hello **world**![/code]")
    assert result == [
        {
            "id": ANY,
            "type": "code",
            "syntax": "python",
            "text": (
                '<span class="hl-n">Hello</span> '
                '<span class="hl-o">**</span>'
                '<span class="hl-n">world</span>'
                '<span class="hl-o">**</span>'
                '<span class="hl-err">!</span>'
            ),
        }
    ]


@pytest.mark.asyncio
async def test_code_bbcode_disables_nested_bbcode(context):
    result, _ = await parse_markup(context, "[code][quote]Hello world![/quote][/code]")
    assert result == [
        {
            "id": ANY,
            "type": "code",
            "syntax": None,
            "text": "[quote]Hello world![/quote]",
        }
    ]
