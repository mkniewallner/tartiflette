from typing import Dict

from tartiflette.language.ast import (
    EnumTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
    InterfaceTypeDefinitionNode,
    ListTypeNode,
    NamedTypeNode,
    NonNullTypeNode,
    ObjectTypeDefinitionNode,
    ScalarTypeDefinitionNode,
    UnionTypeDefinitionNode,
)
from tartiflette.language.ast.base import TypeDefinitionNode
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ValidObjectDefinitionInterfacesRule",)

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


class ValidObjectDefinitionInterfacesRule(ASTValidationRule):
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
        object_field_map = {field.name.value: field for field in node.fields}

        known_interfaces: Dict[str, "NameNode"] = {}
        if node.interfaces:
            for interface_definition in node.interfaces:
                interface_name = interface_definition.name.value
                interface_type = self._known_types.get(interface_name)

                # Unknown interface type should be check elsewhere
                if interface_type is None:
                    continue

                known_interface = known_interfaces.get(interface_name)
                if known_interface:
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Type {object_name} can only implement "
                            f"{interface_name} once.",
                            nodes=[known_interface, interface_definition.name],
                        )
                    )
                    continue

                known_interfaces[interface_name] = interface_definition.name

                # Validate Object implements Interface
                interface_field_map = {
                    interface.name.value: interface
                    for interface in interface_type.fields
                }
                for field_name, interface_field in interface_field_map.items():
                    object_field = object_field_map.get(field_name)

                    if object_field is None:
                        self.context.report_error(
                            graphql_error_from_nodes(
                                "Interface field "
                                f"< {interface_name}.{field_name} > expected "
                                f"but {object_name} does not provide it.",
                                nodes=[interface_field, node],
                            )
                        )
                        continue

                    if not is_type_sub_type_of(
                        self._known_types,
                        object_field.type,
                        interface_field.type,
                    ):
                        self.context.report_error(
                            graphql_error_from_nodes(
                                "Interface field "
                                f"< {interface_name}.{field_name} > expects "
                                f"type < {interface_field.type} > but "
                                f"< {object_name}.{field_name} > is type "
                                f"< {object_field.type} >.",
                                nodes=[
                                    interface_field.type,
                                    object_field.type,
                                ],
                            )
                        )


def is_type_sub_type_of(known_type, maybe_sub_type, super_type):
    if isinstance(maybe_sub_type, NamedTypeNode):
        maybe_sub_type = known_type[maybe_sub_type.name.value]

    if isinstance(super_type, NamedTypeNode):
        super_type = known_type[super_type.name.value]

    if maybe_sub_type is super_type:
        return True

    if isinstance(super_type, NonNullTypeNode):
        if isinstance(maybe_sub_type, NonNullTypeNode):
            return is_type_sub_type_of(
                known_type, maybe_sub_type.type, super_type.type
            )
        return False

    if isinstance(maybe_sub_type, NonNullTypeNode):
        return is_type_sub_type_of(known_type, maybe_sub_type.type, super_type)

    if isinstance(super_type, ListTypeNode):
        if isinstance(maybe_sub_type, ListTypeNode):
            return is_type_sub_type_of(
                known_type, maybe_sub_type.type, super_type.type
            )
        return False

    if isinstance(maybe_sub_type, ListTypeNode):
        return False

    return False
