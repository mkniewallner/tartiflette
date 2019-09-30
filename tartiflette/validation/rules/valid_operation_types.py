from typing import Dict

from tartiflette.language.ast import ObjectTypeDefinitionNode
from tartiflette.language.ast.base import TypeDefinitionNode
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ValidOperationTypesRule",)

_QUERY_OPERATION_TYPE = "query"
_MUTATION_OPERATION_TYPE = "mutation"
_SUBSCRIPTION_OPERATION_TYPE = "subscription"
_DEFAULT_ROOT_OPERATION_NAMES_MAP: Dict[str, str] = {
    _QUERY_OPERATION_TYPE: "Query",
    _MUTATION_OPERATION_TYPE: "Mutation",
    _SUBSCRIPTION_OPERATION_TYPE: "Subscription",
}


class ValidOperationTypesRule(ASTValidationRule):
    """
    TODO:
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: TODO:
        :type context: TODO:
        """
        super().__init__(context)
        self._operation_type_nodes: Dict[str, "OperationDefinitionNode"] = {}
        self._known_types: Dict[str, "TypeDefinitionNode"] = {
            definition_node.name.value: definition_node
            for definition_node in context.document_node.definitions
            if isinstance(definition_node, TypeDefinitionNode)
        }

    def _check_root_operation_validness(
        self, operation_type: str, is_required: bool = False
    ):
        """
        TODO:
        :param operation_type: TODO:
        :param is_required: TODO:
        :type operation_type: TODO:
        :type is_required: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        defined_operation_definition_node = self._operation_type_nodes.get(
            operation_type
        )
        operation_name = (
            defined_operation_definition_node.type.name.value
            if defined_operation_definition_node
            else _DEFAULT_ROOT_OPERATION_NAMES_MAP[operation_type]
        )
        known_type = self._known_types.get(operation_name)

        if (
            not is_required
            and not defined_operation_definition_node
            and not known_type
        ):
            return

        default_operation_type_name = _DEFAULT_ROOT_OPERATION_NAMES_MAP[
            operation_type
        ]

        if not known_type and not defined_operation_definition_node:
            self.context.report_error(
                graphql_error_from_nodes(
                    f"{default_operation_type_name} root type must be "
                    "provided.",
                    nodes=[self.context.document_node],
                )
            )
        elif not isinstance(known_type, ObjectTypeDefinitionNode):
            self.context.report_error(
                graphql_error_from_nodes(
                    f"{default_operation_type_name} root type must be Object "
                    "type.",
                    nodes=[defined_operation_definition_node.type],
                )
            )

    def enter_OperationTypeDefinition(
        self, node: "OperationDefinitionNode", *_
    ):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        self._operation_type_nodes[node.operation_type] = node

    def leave_Document(self, *_):
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        self._check_root_operation_validness(
            _QUERY_OPERATION_TYPE, is_required=True
        )
        self._check_root_operation_validness(_MUTATION_OPERATION_TYPE)
        self._check_root_operation_validness(_SUBSCRIPTION_OPERATION_TYPE)
