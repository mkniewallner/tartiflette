from collections import defaultdict
from typing import Dict, List, Optional, Union

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
from tartiflette.validation.rules.utils import (
    is_introspection_type,
    is_valid_name,
)

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
        self._known_object_types: Dict[str, List["FieldNode"]] = defaultdict(
            list
        )
        self._current_object_type_name: Optional[str] = None

    def enter_ObjectTypeDefinition(self, node: "ObjectTypeDefinitionNode", *_):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        object_name = node.name.value
        self._current_object_type_name = object_name

        if not (
            is_introspection_type(node, object_name)
            and is_valid_name(object_name)
        ):
            self.context.report_error(
                graphql_error_from_nodes(
                    f'Name < {object_name} > must not begin with "__", '
                    "which is reserved by GraphQL introspection.",
                    nodes=[node.name],
                )
            )

    def enter_ObjectTypeExtension(self, node: "ObjectTypeExtensionNode", *_):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        self._current_object_type_name = node.name.value

    def leave_ObjectTypeDefinition(self, *_):
        self._current_object_type_name = None

    def leave_ObjectTypeExtension(self, *_):
        self._current_object_type_name = None

    def enter_FieldDefinition(self, node: "FieldDefinitionNode", *_):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        if not self._current_object_type_name:
            return

        self._known_object_types[self._current_object_type_name].append(node)

    def leave_Document(self, *_):
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        pass
