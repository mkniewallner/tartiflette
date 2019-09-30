from typing import Dict

from tartiflette.language.ast import (
    EnumTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
    InterfaceTypeDefinitionNode,
    ObjectTypeDefinitionNode,
    ScalarTypeDefinitionNode,
    UnionTypeDefinitionNode,
)
from tartiflette.language.ast.base import TypeDefinitionNode
from tartiflette.language.utils import get_wrapped_named_type
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ValidObjectDefinitionsRule",)

_INPUT_TYPES = (
    ScalarTypeDefinitionNode,
    EnumTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
)
_OUTPUT_TYPES = (
    ScalarTypeDefinitionNode,
    ObjectTypeDefinitionNode,
    InterfaceTypeDefinitionNode,
    UnionTypeDefinitionNode,
    EnumTypeDefinitionNode,
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


class ValidObjectDefinitionsRule(ASTValidationRule):
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

    def enter_ObjectTypeDefinition(self, node: "ObjectTypeDefinitionNode", *_):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        object_name = node.name.value

        if not _is_valid_name(object_name):
            self.context.report_error(
                graphql_error_from_nodes(
                    f'Name < {object_name} > must not begin with "__", '
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
                            f"Object type < {object_name} > can only "
                            f"include field {field_name} once.",
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
                if not isinstance(wrapped_field_type, _OUTPUT_TYPES):
                    self.context.report_error(
                        graphql_error_from_nodes(
                            "The type of "
                            f"< {object_name}.{field_name} > must be "
                            f"Output type but got: {field_definition.type}.",
                            nodes=[field_definition.type],
                        )
                    )

                known_argument_names: Dict[str, "NameNode"] = {}

                if field_definition.arguments:
                    for argument_definition in field_definition.arguments:
                        argument_name = argument_definition.name.value

                        known_argument = known_argument_names.get(
                            argument_name
                        )
                        if known_argument:
                            self.context.report_error(
                                graphql_error_from_nodes(
                                    f"Field argument "
                                    f"< {object_name}.{field_name}({argument_name}) > "
                                    f"can only be defined once.",
                                    nodes=[
                                        known_argument,
                                        argument_definition.name,
                                    ],
                                )
                            )
                            continue

                        known_argument_names[
                            argument_name
                        ] = argument_definition.name

                        if not _is_valid_name(argument_name):
                            self.context.report_error(
                                graphql_error_from_nodes(
                                    f"Name < {argument_name} > must not begin with "
                                    '"__", which is reserved by GraphQL '
                                    "introspection.",
                                    nodes=[argument_definition.name],
                                )
                            )

                        wrapped_field_type_name = get_wrapped_named_type(
                            argument_definition.type
                        )
                        wrapped_field_type = (
                            self._known_types.get(
                                wrapped_field_type_name.name.value
                            )
                            if wrapped_field_type_name
                            else None
                        )
                        if not isinstance(wrapped_field_type, _INPUT_TYPES):
                            self.context.report_error(
                                graphql_error_from_nodes(
                                    "The type of "
                                    f"< {object_name}.{field_name}({argument_name}) > "
                                    "must be Input type but got: "
                                    f"{argument_definition.type}.",
                                    nodes=[argument_definition.type],
                                )
                            )
