from difflib import get_close_matches
from typing import Set

from tartiflette.language.ast.base import (
    TypeDefinitionNode,
    TypeSystemDefinitionNode,
    TypeSystemExtensionNode,
)
from tartiflette.utils.errors import did_you_mean, graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("KnownTypeNamesRule",)


_TYPE_SYSTEM_NODES = (TypeSystemDefinitionNode, TypeSystemExtensionNode)


class KnownTypeNamesRule(ASTValidationRule):
    """
    A GraphQL document is only valid if referenced types (specifically
    variable definitions and fragment conditions) are defined by the type
    schema.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: TODO:
        :type context: TODO:
        """
        super().__init__(context)
        schema = context.schema
        self._existing_types: Set[str] = (
            set(schema.type_definitions) if schema else set()
        )
        self._defined_types: Set[str] = {
            definition_node.name.value
            for definition_node in context.document_node.definitions
            if isinstance(definition_node, TypeDefinitionNode)
        }
        self._known_type_names = self._existing_types | self._defined_types

    def enter_NamedType(self, node: "NamedType", *_):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        type_name = node.name.value
        if (
            type_name not in self._existing_types
            and type_name not in self._defined_types
        ):
            suggested_types = get_close_matches(
                type_name, self._known_type_names, n=5
            )
            self.context.report_error(
                graphql_error_from_nodes(
                    f"Unknown type < {type_name} >."
                    + did_you_mean(suggested_types),
                    nodes=[node],
                )
            )
