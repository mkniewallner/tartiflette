from typing import Dict, List

from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueInputFieldNamesRule",)


class UniqueInputFieldNamesRule(ASTValidationRule):
    """
    A GraphQL input object value is only valid if all supplied fields are
    uniquely named.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: TODO:
        :type context: TODO:
        """
        super().__init__(context)
        self._known_name_stack: List[Dict[str, "NameNode"]] = []
        self._known_input_fields: Dict[str, "NameNode"] = {}

    def enter_ObjectValue(self, *_):
        """
        TODO:
        """
        self._known_name_stack.append(self._known_input_fields)
        self._known_input_fields: Dict[str, "NameNode"] = {}

    def leave_ObjectValue(self, *_):
        """
        TODO:
        """
        self._known_input_fields: Dict[
            str, "NameNode"
        ] = self._known_name_stack.pop()

    def enter_ObjectField(self, node: "ObjectFieldNode", *_):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        field_name = node.name.value
        known_input_field = self._known_input_fields.get(field_name)
        if known_input_field:
            self.context.report_error(
                graphql_error_from_nodes(
                    f"There can be only one input field named < {field_name} >.",
                    nodes=[known_input_field, node.name],
                )
            )
        else:
            self._known_input_fields[field_name] = node.name
