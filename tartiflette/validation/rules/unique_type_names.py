from typing import Dict, Union

from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueTypeNamesRule",)


class UniqueTypeNamesRule(ASTValidationRule):
    """
    A GraphQL document is only valid if all defined types have unique names.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: TODO:
        :type context: TODO:
        """
        super().__init__(context)
        self._known_type_names: Dict[str, "NameNode"] = {}

    def _check_type_name_uniqueness(
        self,
        node: Union[
            "ScalarTypeDefinitionNode",
            "ObjectTypeDefinitionNode",
            "InterfaceTypeDefinitionNode",
            "UnionTypeDefinitionNode",
            "EnumTypeDefinitionNode",
            "InputObjectTypeDefinitionNode",
        ],
        *_,
    ):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        type_name = node.name.value

        known_type_name = self._known_type_names.get(type_name)
        if known_type_name:
            self.context.report_error(
                graphql_error_from_nodes(
                    f"There can be only one type named < {type_name} >.",
                    nodes=[known_type_name, node.name],
                )
            )
        else:
            self._known_type_names[type_name] = node.name

        return SKIP

    enter_ScalarTypeDefinition = _check_type_name_uniqueness
    enter_ObjectTypeDefinition = _check_type_name_uniqueness
    enter_InterfaceTypeDefinition = _check_type_name_uniqueness
    enter_UnionTypeDefinition = _check_type_name_uniqueness
    enter_EnumTypeDefinition = _check_type_name_uniqueness
    enter_InputObjectTypeDefinition = _check_type_name_uniqueness
