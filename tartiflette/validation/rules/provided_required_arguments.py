from typing import Any, Dict

from tartiflette.language.ast import DirectiveDefinitionNode, NonNullTypeNode
from tartiflette.language.ast.base import Node
from tartiflette.types.non_null import GraphQLNonNull
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ProvidedRequiredArgumentsOnDirectivesRule",)


def _is_required_argument(argument: "GraphQLArgument") -> bool:
    """
    TODO:
    :param argument: TODO:
    :type argument: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return (
        isinstance(argument.graphql_type, GraphQLNonNull)
        and argument.default_value is None
    )


def _is_required_argument_node(argument: "ArgumentNode") -> bool:
    """
    TODO:
    :param argument: TODO:
    :type argument: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return (
        isinstance(argument.type, NonNullTypeNode)
        and argument.default_value is None
    )


class ProvidedRequiredArgumentsOnDirectivesRule(ASTValidationRule):
    """
    A directive is only valid if all required (non-null without a default
    value) arguments have been provided.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: TODO:
        :type context: TODO:
        """
        super().__init__(context)
        self._directive_required_arguments: Dict[str, Dict[str, Any]] = (
            {
                directive.name: {
                    argument_name: argument
                    for argument_name, argument in directive.arguments.items()
                    if _is_required_argument(argument)
                }
                for directive in context.schema.directive_definitions.values()
            }
            if context.schema
            else {}
        )
        self._directive_required_arguments.update(
            {
                directive_definition.name.value: (
                    {
                        argument.name.value: argument
                        for argument in directive_definition.arguments
                        if _is_required_argument_node(argument)
                    }
                    if directive_definition.arguments
                    else {}
                )
                for directive_definition in context.document_node.definitions
                if isinstance(directive_definition, DirectiveDefinitionNode)
            }
        )

    def leave_Directive(self, node: "DirectiveNode", *_):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        directive_name = node.name.value
        required_arguments = self._directive_required_arguments.get(
            directive_name
        )

        if required_arguments:
            argument_nodes = {
                argument_node.name.value: argument_node
                for argument_node in node.arguments or []
            }
            for argument_name in required_arguments:
                if argument_name not in argument_nodes:
                    required_argument = required_arguments[argument_name]
                    argument_type = (
                        required_argument.type
                        if isinstance(required_argument, Node)
                        else required_argument.graphql_type
                    )

                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Directive < {directive_name} > argument "
                            f"< {argument_name} > of type < {argument_type} > "
                            "required, but it was not provided.",
                            nodes=[node],
                        )
                    )
