from typing import Dict, Union

from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueOperationTypesRule",)


class UniqueOperationTypesRule(ASTValidationRule):
    """
    A GraphQL document is only valid if it has only one type per operation.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: TODO:
        :type context: TODO:
        """
        super().__init__(context)
        self._known_operation_types: Dict[
            str, "OperationTypeDefinitionNode"
        ] = {}

    def _check_operation_type_uniqueness(
        self, node: Union["SchemaDefinitionNode", "SchemaExtensionNode"], *_
    ):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        if node.operation_type_definitions:
            for operation_type_definition in node.operation_type_definitions:
                operation_type: str = operation_type_definition.operation_type
                known_operation_type = self._known_operation_types.get(
                    operation_type
                )
                if known_operation_type:
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"There can be only one < {operation_type} > type "
                            "in schema.",
                            nodes=[
                                known_operation_type,
                                operation_type_definition,
                            ],
                        )
                    )
                else:
                    self._known_operation_types[
                        operation_type
                    ] = operation_type_definition
        return SKIP

    enter_SchemaDefinition = _check_operation_type_uniqueness
    enter_SchemaExtension = _check_operation_type_uniqueness
