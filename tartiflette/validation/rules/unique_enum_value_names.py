from typing import Any, Dict, Union

from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueEnumValueNamesRule",)


class UniqueEnumValueNamesRule(ASTValidationRule):
    """
    A GraphQL enum type is only valid if all its values are uniquely named.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: TODO:
        :type context: TODO:
        """
        super().__init__(context)
        self._known_enum_value_names: Dict[str, "NameNode"] = {}

    def _check_enum_value_uniqueness(
        self,
        node: Union["EnumTypeDefinitionNode", "EnumTypeExtensionNode"],
        *_,
    ):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        if node.values:
            enum_type_name = node.name.value
            enum_value_names = self._known_enum_value_names.setdefault(
                enum_type_name, {}
            )
            for value_definition in node.values:
                enum_value_name = value_definition.name.value
                known_enum_value = enum_value_names.get(enum_value_name)
                if known_enum_value:
                    self.context.report_error(
                        graphql_error_from_nodes(
                            "Enum value "
                            f"< {enum_type_name}.{enum_value_name} > "
                            "can only be defined once.",
                            nodes=[known_enum_value, value_definition.name],
                        )
                    )
                else:
                    enum_value_names[enum_value_name] = value_definition.name
        return SKIP

    enter_EnumTypeDefinition = _check_enum_value_uniqueness
    enter_EnumTypeExtension = _check_enum_value_uniqueness
