from difflib import get_close_matches
from typing import Dict, Union

from tartiflette.language.ast import (
    EnumTypeDefinitionNode,
    EnumTypeExtensionNode,
    InputObjectTypeDefinitionNode,
    InputObjectTypeExtensionNode,
    InterfaceTypeDefinitionNode,
    InterfaceTypeExtensionNode,
    ObjectTypeDefinitionNode,
    ObjectTypeExtensionNode,
    ScalarTypeDefinitionNode,
    ScalarTypeExtensionNode,
    UnionTypeDefinitionNode,
    UnionTypeExtensionNode,
)
from tartiflette.language.ast.base import TypeDefinitionNode
from tartiflette.types.enum import GraphQLEnumType
from tartiflette.types.input_object import GraphQLInputObjectType
from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.object import GraphQLObjectType
from tartiflette.types.scalar import GraphQLScalarType
from tartiflette.types.union import GraphQLUnionType
from tartiflette.utils.errors import did_you_mean, graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("PossibleTypeExtensionsRule",)


_EXTENSION_TO_TYPE_NAME = {
    ScalarTypeExtensionNode: "scalar",
    ObjectTypeExtensionNode: "object",
    InterfaceTypeExtensionNode: "interface",
    UnionTypeExtensionNode: "union",
    EnumTypeExtensionNode: "enum",
    InputObjectTypeExtensionNode: "input object",
}

_DEFINITION_TO_EXTENSION_CLASS = {
    ScalarTypeDefinitionNode: ScalarTypeExtensionNode,
    ObjectTypeDefinitionNode: ObjectTypeExtensionNode,
    InterfaceTypeDefinitionNode: InterfaceTypeExtensionNode,
    UnionTypeDefinitionNode: UnionTypeExtensionNode,
    EnumTypeDefinitionNode: EnumTypeExtensionNode,
    InputObjectTypeDefinitionNode: InputObjectTypeExtensionNode,
}

_GRAPHQL_TYPE_TO_EXTENSION_CLASS = {
    GraphQLScalarType: ScalarTypeExtensionNode,
    GraphQLObjectType: ObjectTypeExtensionNode,
    GraphQLInterfaceType: InterfaceTypeExtensionNode,
    GraphQLUnionType: UnionTypeExtensionNode,
    GraphQLEnumType: EnumTypeExtensionNode,
    GraphQLInputObjectType: InputObjectTypeExtensionNode,
}


class PossibleTypeExtensionsRule(ASTValidationRule):
    """
    A type extension is only valid if the type is defined and has the same
    kind.
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

    def _check_extension_validness(
        self,
        node: Union[
            "InputObjectTypeExtensionNode",
            "InterfaceTypeExtensionNode",
            "ScalarTypeExtensionNode",
            "ObjectTypeExtensionNode",
            "UnionTypeExtensionNode",
            "EnumTypeExtensionNode",
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
        definition_node = self._known_types.get(type_name)

        if definition_node:
            expected_kind = _DEFINITION_TO_EXTENSION_CLASS.get(
                type(definition_node)
            )
            if not isinstance(node, expected_kind):
                kind = _EXTENSION_TO_TYPE_NAME.get(
                    expected_kind, "unknown type"
                )
                self.context.report_error(
                    graphql_error_from_nodes(
                        f"Cannot extend non-{kind} type < {type_name} >.",
                        nodes=[definition_node, node],
                    )
                )
        else:
            suggested_types = get_close_matches(
                type_name, list(self._known_types), n=5
            )
            self.context.report_error(
                graphql_error_from_nodes(
                    f"Cannot extend type < {type_name} > because it is not "
                    "defined." + did_you_mean(suggested_types),
                    nodes=[node.name],
                )
            )

    enter_InputObjectTypeExtension = _check_extension_validness
    enter_InterfaceTypeExtension = _check_extension_validness
    enter_ScalarTypeExtension = _check_extension_validness
    enter_ObjectTypeExtension = _check_extension_validness
    enter_UnionTypeExtension = _check_extension_validness
    enter_EnumTypeExtension = _check_extension_validness
