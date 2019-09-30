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

__all__ = ("ValidInputObjectDefinitionsRule",)

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


class ValidInputObjectDefinitionsRule(ASTValidationRule):
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

    def enter_InputObjectTypeDefinition(
        self, node: "InputObjectTypeDefinitionNode", *_
    ):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        input_object_name = node.name.value

        if not _is_valid_name(input_object_name):
            self.context.report_error(
                graphql_error_from_nodes(
                    f'Name < {input_object_name} > must not begin with "__", '
                    "which is reserved by GraphQL introspection.",
                    nodes=[node.name],
                )
            )

        known_fields: Dict[str, "NameNode"] = {}
        if node.fields:
            for field_definition in node.fields:
                field_name = field_definition.name.value

                known_field = known_fields.get(field_name)
                if known_field:
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Input object type < {input_object_name} > can "
                            f"only include field {field_name} once.",
                            nodes=[known_field, field_definition.name],
                        )
                    )
                    continue

                known_fields[field_name] = field_definition.name

                if not _is_valid_name(field_name):
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Name < {field_name} > must not begin with "
                            '"__", which is reserved by GraphQL '
                            "introspection.",
                            nodes=[field_definition.name],
                        )
                    )

                wrapped_field_type_name = get_wrapped_named_type(
                    field_definition.type
                )
                wrapped_field_type = (
                    self._known_types.get(wrapped_field_type_name.name.value)
                    if wrapped_field_type_name
                    else None
                )
                if not isinstance(wrapped_field_type, _INPUT_TYPES):
                    self.context.report_error(
                        graphql_error_from_nodes(
                            "The type of "
                            f"< {input_object_name}.{field_name} > must be "
                            f"Input type but got: {field_definition.type}.",
                            nodes=[field_definition.type],
                        )
                    )
