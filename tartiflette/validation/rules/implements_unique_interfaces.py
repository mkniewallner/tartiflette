from typing import Dict, Union

from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ImplementsUniqueInterfacesRule",)


class ImplementsUniqueInterfacesRule(ASTValidationRule):
    """
    TODO:
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: TODO:
        :type context: TODO:
        """
        super().__init__(context)
        self._known_implemented_interface_names: Dict[
            str, Dict[str, "NameNode"]
        ] = {}

    def check_implements_unique_interfaces(
        self,
        node: Union["ObjectTypeDefinitionNode", "ObjectTypeExtensionNode"],
        *_,
    ):
        """
        TODO:
        :param node: TODO:
        :type node: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        if node.interfaces:
            type_name = node.name.value
            self._known_implemented_interface_names.setdefault(type_name, {})

            interface_names = self._known_implemented_interface_names[
                type_name
            ]
            for implemented_interface in node.interfaces:
                interface_name = implemented_interface.name.value
                known_interface = interface_names.get(interface_name)
                if known_interface:
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Type < {type_name} > can only implement "
                            f"< {interface_name} > once.",
                            nodes=[
                                known_interface,
                                implemented_interface.name,
                            ],
                        )
                    )
                else:
                    interface_names[
                        interface_name
                    ] = implemented_interface.name
        return SKIP

    enter_ObjectTypeDefinition = check_implements_unique_interfaces
    enter_ObjectTypeExtension = check_implements_unique_interfaces
