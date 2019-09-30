from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("LoneSchemaDefinitionRule",)


class LoneSchemaDefinitionRule(ASTValidationRule):
    """
    A GraphQL document is only valid if it contains only one schema definition.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: TODO:
        :type context: TODO:
        """
        super().__init__(context)
        self._is_already_defined = False

    def enter_SchemaDefinition(self, node: "SchemaDefinitionNode", *_):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        if self._is_already_defined:
            self.context.report_error(
                graphql_error_from_nodes(
                    "Must provide only one schema definition.", nodes=[node]
                )
            )
        self._is_already_defined = True
