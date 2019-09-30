from tartiflette.language.ast import (
    EnumTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
    InterfaceTypeDefinitionNode,
    ObjectTypeDefinitionNode,
    UnionTypeDefinitionNode,
)
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ValidTypeDefinitionsRule",)


_VALIDATORS = {
    InputObjectTypeDefinitionNode: (),
    InterfaceTypeDefinitionNode: (),
    ObjectTypeDefinitionNode: (),
    UnionTypeDefinitionNode: (),
    EnumTypeDefinitionNode: (),
}


class ValidTypeDefinitionsRule(ASTValidationRule):
    """
    TODO:
    """

    enter_InputObjectTypeDefinition = None
    enter_InterfaceTypeDefinition = None
    enter_ScalarTypeDefinition = None
    enter_ObjectTypeDefinition = None
    enter_UnionTypeDefinition = None
    enter_EnumTypeDefinition = None

    enter_InputObjectTypeExtension = None
    enter_InterfaceTypeExtension = None
    enter_ScalarTypeExtension = None
    enter_ObjectTypeExtension = None
    enter_UnionTypeExtension = None
    enter_EnumTypeExtension = None
