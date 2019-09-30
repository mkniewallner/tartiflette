from tartiflette.language.ast.base import TypeSystemDefinitionNode
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ValidNamesRule",)

_INTROSPECTION_TYPE_NAMES = (
    "__Schema",
    "__Directive",
    "__DirectiveLocation",
    "__Type",
    "__Field",
    "__InputValue",
    "__EnumValue",
    "__TypeKind",
)


def _is_introspection_type(node: "Node", name: str) -> bool:
    """
    Determines whether or not a name related to an AST node correspond to an
    introspection type.
    :param node: AST node related to the name
    :param name: name of the type
    :type node: Node
    :type name: str
    :return: whether or not a name related to an AST node correspond to an
    introspection type
    :rtype: bool
    """
    return (
        isinstance(node, TypeSystemDefinitionNode)
        and name in _INTROSPECTION_TYPE_NAMES
    )


class ValidNamesRule(ASTValidationRule):
    """
    Validates that user did not defined any types, fields, arguments, or any
    other type system artifact with two leading underscores.
    """

    def check_name_validness(self, node, *_):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        name = node.name.value
        if not _is_introspection_type(node, name) and name.startswith("__"):
            self.context.report_error(
                graphql_error_from_nodes(
                    f'Name < {name} > must not begin with "__", which is '
                    "reserved by GraphQL introspection.",
                    nodes=[node.name],
                )
            )

    enter_InputObjectTypeDefinition = check_name_validness
    enter_InterfaceTypeDefinition = check_name_validness
    enter_InputValueDefinition = check_name_validness
    enter_ScalarTypeDefinition = check_name_validness
    enter_ObjectTypeDefinition = check_name_validness
    enter_DirectiveDefinition = check_name_validness
    enter_UnionTypeDefinition = check_name_validness
    enter_EnumValueDefinition = check_name_validness
    enter_EnumTypeDefinition = check_name_validness
    enter_FieldDefinition = check_name_validness
