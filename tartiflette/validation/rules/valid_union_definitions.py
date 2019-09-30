from typing import Dict

from tartiflette.language.ast import (
    EnumTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
    ObjectTypeDefinitionNode,
    ScalarTypeDefinitionNode,
)
from tartiflette.language.ast.base import TypeDefinitionNode
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ValidUnionDefinitionsRule",)

_INPUT_TYPES = (
    ScalarTypeDefinitionNode,
    EnumTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
)


def _is_valid_name(name: str) -> bool:
    """
    TODO:
    :param name: TODO:
    :type name: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return not name.startswith("__")


class ValidUnionDefinitionsRule(ASTValidationRule):
    """
    TODO:
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: TODO:
        :type context: TODO:
        """
        super().__init__(context)
        self._known_types: Dict[str, "TypeDefinitionNode"] = {
            definition_node.name.value: definition_node
            for definition_node in context.document_node.definitions
            if isinstance(definition_node, TypeDefinitionNode)
        }

    def enter_UnionTypeDefinition(self, node: "UnionTypeDefinitionNode", *_):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        union_name = node.name.value

        if not _is_valid_name(union_name):
            self.context.report_error(
                graphql_error_from_nodes(
                    f'Name < {union_name} > must not begin with "__", '
                    "which is reserved by GraphQL introspection.",
                    nodes=[node.name],
                )
            )

        known_members: Dict[str, "NameNode"] = {}

        if node.types:
            for member_definition in node.types:
                member_name = member_definition.name.value

                known_member = known_members.get(member_name)
                if known_member:
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Union type < {union_name} > can only include "
                            f"type {member_name} once.",
                            nodes=[known_member, member_definition.name],
                        )
                    )
                    continue

                known_members[member_name] = member_definition.name

                wrapped_field_type = self._known_types.get(
                    member_definition.name.value
                )
                if not isinstance(
                    wrapped_field_type, ObjectTypeDefinitionNode
                ):
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Union type < {union_name} > can only include "
                            "Object types, it cannot include "
                            f"< {member_definition} >.",
                            nodes=[member_definition],
                        )
                    )
