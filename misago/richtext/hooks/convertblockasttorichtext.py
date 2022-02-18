from typing import Optional, Protocol

from ...context import Context
from ...hooks import FilterHook
from ..types import ParsedMarkupMetadata, RichTextBlock


class ConvertBlockAstToRichTextAction(Protocol):
    def __call__(
        self, context: Context, ast: dict, metadata: ParsedMarkupMetadata
    ) -> Optional[RichTextBlock]:
        ...


class ConvertBlockAstToRichTextFilter(Protocol):
    def __call__(
        self,
        action: ConvertBlockAstToRichTextAction,
        context: Context,
        ast: dict,
        metadata: ParsedMarkupMetadata,
    ) -> Optional[RichTextBlock]:
        ...


class ConvertBlockAstToRichTextHook(
    FilterHook[ConvertBlockAstToRichTextAction, ConvertBlockAstToRichTextFilter]
):
    is_async = False

    def call_action(
        self,
        action: ConvertBlockAstToRichTextAction,
        context: Context,
        ast: dict,
        metadata: ParsedMarkupMetadata,
    ) -> Optional[RichTextBlock]:
        return self.filter(action, context, ast, metadata)


convert_block_ast_to_rich_text_hook = ConvertBlockAstToRichTextHook()
