from tartiflette.constants.introspection import INTROSPECTION_TYPE_NAMES
from tartiflette.language.ast.base import TypeSystemDefinitionNode

__all__ = ("is_introspection_type", "is_valid_name")


def is_introspection_type(node: "Node", name: str) -> bool:
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
        and name in INTROSPECTION_TYPE_NAMES
    )


def is_valid_name(name: str) -> bool:
    """
    TODO:
    :param name: TODO:
    :type name: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return not name.startswith("__")
