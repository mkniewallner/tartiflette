from typing import List, Optional

from tartiflette.language.visitor.visit import visit
from tartiflette.language.visitor.visitor import ParallelVisitor
from tartiflette.validation.context import ASTValidationContext
from tartiflette.validation.rules import SPECIFIED_SDL_RULES


def validate_sdl(
    document_node: "DocumentNode",
    rules: Optional[List["ValidationRule"]] = None,
) -> List["TartifletteError"]:
    """
    TODO:
    :param document_node: TODO:
    :param rules: TODO:
    :type document_node: TODO:
    :type rules: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    if rules is None:
        rules = SPECIFIED_SDL_RULES

    context = ASTValidationContext(document_node)
    visitors = [rule(context) for rule in rules]
    visit(document_node, ParallelVisitor(visitors))
    return context.errors
