# Type System

## Type System Definition

### Schema Definition

[x] `LoneSchemaDefinitionRule`: when using the type system definition language, a document must include at most one schema definition.
[x] `UniqueTypeNamesRule`: all types within a GraphQL schema must have unique names. No two provided types may have the same name. No provided type may have a name which conflicts with any built in types (including Scalar and Introspection types).
[x] `UniqueDirectiveNamesRule`: all directives within a GraphQL schema must have unique names.
[x] `ValidOperationTypesRule`:
    [x] The query root operation type must be provided and must be an Object type.
    [x] The mutation root operation type is optional; if it is not provided, the service does not support mutations. If it is provided, it must be an Object type.
    [x] Similarly, the subscription root operation type is also optional; if it is not provided, the service does not support subscriptions. If it is provided, it must be an Object type.
    [x] While any type can be the root operation type for a GraphQL operation, the type system definition language can omit the schema definition when the query, mutation, and subscription root types are named Query, Mutation, and Subscription respectively.
[ ] `ValidNamesRule`: all types and directives defined within a schema must not have a name which begins with `__` (two underscores), as this is used exclusively by GraphQL’s introspection system.

### Type Definition

#### Scalar Type Definition

N/A

#### Object Type Definition

[ ] `DefineFields`: must define one or more fields
[x] `ValidObjectDefinitionsRule`: each field must have a unique name within the object type
[x] `ValidObjectDefinitionsRule`: each field must not have a name which begins with the characters `__`
[x] `ValidObjectDefinitionsRule`: each field must return a type which is an output type
[x] `ValidObjectDefinitionsRule`: each argument of each field must have a unique name within the field
[x] `ValidObjectDefinitionsRule`: each argument of each field must not have a name which begins with the characters `__`
[x] `ValidObjectDefinitionsRule`: each argument of each field must accept a type which is an input type
[x] `ImplementsUniqueInterfacesRule`: may declare that it implements one or more unique interfaces
[ ] `FollowsImplementedInterfaces`: must be a super‐set of all interfaces it implements:
    1. The object type must include a field of the same name for every field defined in an interface.
        1. The object field must be of a type which is equal to or a sub‐type of the interface field (covariant).
            1. An object field type is a valid sub‐type if it is equal to (the same type as) the interface field type.
            2. An object field type is a valid sub‐type if it is an Object type and the interface field type is either an Interface type or a Union type and the object field type is a possible type of the interface field type.
            3. An object field type is a valid sub‐type if it is a List type and the interface field type is also a List type and the list‐item type of the object field type is a valid sub‐type of the list‐item type of the interface field type.
            4. An object field type is a valid sub‐type if it is a Non‐Null variant of a valid sub‐type of the interface field type.
        2. The object field must include an argument of the same name for every argument defined in the interface field.
            1. The object field argument must accept the same type (invariant) as the interface field argument.
        3. The object field may include additional arguments not defined in the interface field, but any additional argument must not be required, e.g. must not be of a non‐nullable type.

#### Interface Type Definition

[ ] `DefineFields`: must define one or more fields
[x] `ValidInterfaceDefinitionsRule`: each field must have a unique name within the interface type
[x] `ValidInterfaceDefinitionsRule`: each field must not have a name which begins with the characters `__`
[x] `ValidInterfaceDefinitionsRule`: each field must return a type which is an output type
[x] `ValidInterfaceDefinitionsRule`: each argument of each field must have a unique name within the field
[x] `ValidInterfaceDefinitionsRule`: each argument of each field must not have a name which begins with the characters `__`
[x] `ValidInterfaceDefinitionsRule`: each argument of each field must accept a type which is an input type

#### Union Type Definition

[ ] `DefineMember`: must include one or more member types
[x] `ValidUnionDefinitionsRule`: must not have a name which begins with the characters `__`
[x] `ValidUnionDefinitionsRule`: must include unique member types
[x] `ValidUnionDefinitionsRule`: member types of a Union type must all be object types

#### Enum Type Definition

[ ] `DefineEnumValues`: must define one or more enum values
[x] `ValidEnumDefinitionsRule`: must not have a name which begins with the characters `__`
[x] `ValidEnumDefinitionsRule`: each enum value must not have a name which begins with the characters `__`
[x] `UniqueEnumValueNamesRule`: must define unique enum values

#### InputObject Type Definition

[ ] `DefineInputFields`: must define one or more input fields
[x] `ValidInputObjectDefinitionsRule`: must not have a name which begins with the characters `__`
[x] `ValidInputObjectDefinitionsRule`: each input field must have a unique name within the input object type
[x] `ValidInputObjectDefinitionsRule`: each input field must not have a name which begins with the characters `__`
[x] `ValidInputObjectDefinitionsRule`: each input field must return a type which is an input type

### Wrapping Type

#### Non-Null Type

[ ] `NonNestedNonNullable`: must not wrap another Non‐Null type

### Directive Definition

[ ] `NonDirectRecursiveReference`: must not contain the use of a directive which references itself directly
[ ] `NonIndirectRecursiveReference`: must not contain the use of a directive which references itself indirectly by referencing a Type or Directive which transitively includes a reference to this directive
[x] `ValidDirectiveDefinitionsRule`: must not have a name which begins with the characters `__`
[x] `ValidDirectiveDefinitionsRule`: each argument must have a unique name within the directive
[x] `ValidDirectiveDefinitionsRule`: each argument must not have a name which begins with the characters `__`
[x] `ValidDirectiveDefinitionsRule`: each argument must accept a type which is an input type

## Type System Extensions

### Schema Extension

[ ] `AlreadyDefinedSchema`: must already be defined
[ ] `NonAlreadyDefinedDirective`: any directives provided must not already apply to the original Schema

### Type Extension

#### Scalar Type Extension

[ ] `AlreadyDefinedScalar`: the named type must already be defined and must be a Scalar type
[ ] `NonAlreadyDefinedDirective`: any directives provided must not already apply to the original Scalar type

#### Object Type Extension

#### Interface Type Extension

#### Union Type Extension

#### Enum Type Extension

#### InputObject Type Extension

## Misc

### Reserved Names
