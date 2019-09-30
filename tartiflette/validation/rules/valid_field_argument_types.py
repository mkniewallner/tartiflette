from typing import Dict

from tartiflette.language.ast import (
    EnumTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
    ScalarTypeDefinitionNode,
)
from tartiflette.language.ast.base import TypeDefinitionNode
from tartiflette.language.utils import get_wrapped_named_type
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ValidFieldArgumentTypesRule",)

_INPUT_TYPES = (
    ScalarTypeDefinitionNode,
    EnumTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
)


class ValidFieldArgumentTypesRule(ASTValidationRule):
    """
    TODO:
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: TODO:
        :type context: TODO:
        """
        super().__init__(context)
        self._defined_types: Dict[str, "TypeDefinitionNode"] = {
            definition_node.name.value: definition_node
            for definition_node in context.document_node.definitions
            if isinstance(definition_node, TypeDefinitionNode)
        }

    def enter_FieldDefinition(
        self, node: "FieldDefinitionNode", _, __, ___, ancestors
    ):
        if node.arguments:
            parent_name = ancestors[-1].name.value

            for argument_definition in node.arguments:
                wrapped_field_type_name = get_wrapped_named_type(
                    argument_definition.type
                )
                wrapped_field_type = (
                    self._defined_types.get(wrapped_field_type_name.name.value)
                    if wrapped_field_type_name
                    else None
                )

                if not isinstance(wrapped_field_type, _INPUT_TYPES):
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"The type of < {parent_name}.{node.name.value}"
                            f"({argument_definition.name.value}:) must be "
                            f"Input type but got: {argument_definition.type}.",
                            nodes=[argument_definition.type],
                        )
                    )
