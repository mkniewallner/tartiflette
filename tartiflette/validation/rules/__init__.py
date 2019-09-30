from .known_argument_names import KnownArgumentNamesOnDirectivesRule
from .known_directives import KnownDirectivesRule
from .known_type_names import KnownTypeNamesRule
from .lone_schema_definition import LoneSchemaDefinitionRule
from .possible_type_extensions import PossibleTypeExtensionsRule
from .provided_required_arguments import (
    ProvidedRequiredArgumentsOnDirectivesRule,
)
from .unique_argument_names import UniqueArgumentNamesRule
from .unique_directive_names import UniqueDirectiveNamesRule
from .unique_directives_per_location import UniqueDirectivesPerLocationRule
from .unique_enum_value_names import UniqueEnumValueNamesRule
from .unique_field_definition_names import UniqueFieldDefinitionNamesRule
from .unique_input_field_names import UniqueInputFieldNamesRule
from .unique_operation_types import UniqueOperationTypesRule
from .unique_type_names import UniqueTypeNamesRule
from .valid_directive_definitions import ValidDirectiveDefinitionsRule
from .valid_enum_definitions import ValidEnumDefinitionsRule
from .valid_field_argument_types import ValidFieldArgumentTypesRule
from .valid_field_definition_types import ValidFieldDefinitionTypesRule
from .valid_input_object_definitions import ValidInputObjectDefinitionsRule
from .valid_interface_definitions import ValidInterfaceDefinitionsRule
from .valid_names import ValidNamesRule
from .valid_object_definition_interfaces import (
    ValidObjectDefinitionInterfacesRule,
)
from .valid_object_definitions import ValidObjectDefinitionsRule
from .valid_operation_types import ValidOperationTypesRule
from .valid_union_definitions import ValidUnionDefinitionsRule

SPECIFIED_SDL_RULES = [
    # From GraphQL.js
    LoneSchemaDefinitionRule,  # CHECKED
    UniqueOperationTypesRule,  # CHECKED
    UniqueTypeNamesRule,  # CHECKED
    UniqueEnumValueNamesRule,  # CHECKED
    UniqueFieldDefinitionNamesRule,  # CHECKED
    UniqueDirectiveNamesRule,  # CHECKED
    KnownTypeNamesRule,  # CHECKED - Used on query validation too
    KnownDirectivesRule,  # CHECKED - Used on query validation too
    UniqueDirectivesPerLocationRule,  # CHECKED - Used on query validation too
    PossibleTypeExtensionsRule,  # CHECKED
    KnownArgumentNamesOnDirectivesRule,  # CHECKED - Used on query validation too
    UniqueArgumentNamesRule,  # CHECKED - Used on query validation too
    UniqueInputFieldNamesRule,  # CHECKED - Used on query validation too
    ProvidedRequiredArgumentsOnDirectivesRule,  # CHECKED - Used on query validation too
    # From Tartiflette
    ValidOperationTypesRule,
    ValidDirectiveDefinitionsRule,
    # ValidFieldDefinitionTypesRule,
    # ValidFieldArgumentTypesRule,
    # ValidNamesRule,
    # ValidUnionDefinitionsRule,
    # ValidInterfaceDefinitionsRule,
    # ValidEnumDefinitionsRule,
    # ValidInputObjectDefinitionsRule,
    # ValidObjectDefinitionsRule,
    # ValidObjectDefinitionInterfacesRule,
]

__all__ = ("SPECIFIED_SDL_RULES",)
