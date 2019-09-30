from typing import Dict

from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueArgumentNamesRule",)


class UniqueArgumentNamesRule(ASTValidationRule):
    """
    A GraphQL field or directive is only valid if all supplied arguments are
    uniquely named.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: TODO:
        :type context: TODO:
        """
        super().__init__(context)
        self._known_argument_names: Dict[str, "NameNode"] = {}

    def enter_Field(self, *_):
        """
        TODO:
        """
        self._known_argument_names: Dict[str, "NameNode"] = {}

    def enter_Directive(self, *_):
        """
        TODO:
        """
        self._known_argument_names: Dict[str, "NameNode"] = {}

    def enter_Argument(self, node: "ArgumentNode", *_):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        argument_name = node.name.value
        known_argument = self._known_argument_names.get(argument_name)
        if known_argument:
            self.context.report_error(
                graphql_error_from_nodes(
                    "There can be only one argument named "
                    f"< {argument_name} >.",
                    nodes=[known_argument, node.name],
                )
            )
        else:
            self._known_argument_names[argument_name] = node.name
        return SKIP
