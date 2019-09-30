from tartiflette.language.ast import EnumTypeDefinitionNode
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ValidEnumDefinitionsRule",)


def _is_valid_name(name: str) -> bool:
    """
    TODO:
    :param name: TODO:
    :type name: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return not name.startswith("__")


class ValidEnumDefinitionsRule(ASTValidationRule):
    """
    TODO:
    """

    def enter_EnumTypeDefinition(self, node: "EnumTypeDefinitionNode", *_):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        enum_name = node.name.value

        if not _is_valid_name(enum_name):
            self.context.report_error(
                graphql_error_from_nodes(
                    f'Name < {enum_name} > must not begin with "__", which is '
                    "reserved by GraphQL introspection.",
                    nodes=[node.name],
                )
            )

        if node.values:
            for enum_value_definition in node.values:
                enum_value_name = enum_value_definition.name.value
                if not _is_valid_name(enum_value_name):
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Name < {enum_value_name} > must not begin with "
                            '"__", which is reserved by GraphQL '
                            "introspection.",
                            nodes=[enum_value_definition.name],
                        )
                    )
