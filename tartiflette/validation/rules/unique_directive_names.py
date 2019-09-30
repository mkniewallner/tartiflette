from typing import Dict

from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueDirectiveNamesRule",)


class UniqueDirectiveNamesRule(ASTValidationRule):
    """
    A GraphQL document is only valid if all defined directives have unique
    names.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: TODO:
        :type context: TODO:
        """
        super().__init__(context)
        self._known_directive_names: Dict[str, "NameNode"] = {}

    def enter_DirectiveDefinition(self, node: "DirectiveDefinitionNode", *_):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        directive_name = node.name.value

        known_directive_name = self._known_directive_names.get(directive_name)
        if known_directive_name:
            self.context.report_error(
                graphql_error_from_nodes(
                    "There can be only one directive named "
                    f"< {directive_name} >.",
                    nodes=[known_directive_name, node.name],
                )
            )
        else:
            self._known_directive_names[directive_name] = node.name

        return SKIP
