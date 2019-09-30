# Type System

## Type System Definition

### Schema Definition

* All types within a GraphQL schema must have unique names. No two provided types may have the same name. No provided type may have a name which conflicts with any built in types (including Scalar and Introspection types).
* All directives within a GraphQL schema must have unique names.
* All types and directives defined within a schema must not have a name which begins with `__` (two underscores), as this is used exclusively by GraphQL’s introspection system.
* The query root operation type must be provided and must be an Object type.
* The mutation root operation type is optional; if it is not provided, the service does not support mutations. If it is provided, it must be an Object type.
* Similarly, the subscription root operation type is also optional; if it is not provided, the service does not support subscriptions. If it is provided, it must be an Object type.
* When using the type system definition language, a document must include at most one schema definition.
* While any type can be the root operation type for a GraphQL operation, the type system definition language can omit the schema definition when the query, mutation, and subscription root types are named Query, Mutation, and Subscription respectively.

### Type Definition

#### Scalar Type Definition

* GraphQL provides a basic set of well‐defined Scalar types. A GraphQL server should support all of these types, and a GraphQL server which provide a type by these names must adhere to the behavior described below.

#### Object Type Definition

* All fields defined within an Object type must not have a name which begins with `__` (two underscores), as this is used exclusively by GraphQL’s introspection system.

```
1. An Object type must define one or more fields.
2. For each field of an Object type:
    1. The field must have a unique name within that Object type; no two fields may share the same name.
    2. The field must not have a name which begins with the characters "__" (two underscores).
    3. The field must return a type where IsOutputType(fieldType) returns true.
    4. For each argument of the field:
        1. The argument must not have a name which begins with the characters "__" (two underscores).
        2. The argument must accept a type where IsInputType(argumentType) returns true.
3. An object type may declare that it implements one or more unique interfaces.
4. An object type must be a super‐set of all interfaces it implements:
    1. The object type must include a field of the same name for every field defined in an interface.
        1. The object field must be of a type which is equal to or a sub‐type of the interface field (covariant).
            1. An object field type is a valid sub‐type if it is equal to (the same type as) the interface field type.
            2. An object field type is a valid sub‐type if it is an Object type and the interface field type is either an Interface type or a Union type and the object field type is a possible type of the interface field type.
            3. An object field type is a valid sub‐type if it is a List type and the interface field type is also a List type and the list‐item type of the object field type is a valid sub‐type of the list‐item type of the interface field type.
            4. An object field type is a valid sub‐type if it is a Non‐Null variant of a valid sub‐type of the interface field type.
        2. The object field must include an argument of the same name for every argument defined in the interface field.
            1. The object field argument must accept the same type (invariant) as the interface field argument.
        3. The object field may include additional arguments not defined in the interface field, but any additional argument must not be required, e.g. must not be of a non‐nullable type.
```

* All arguments defined within a field must not have a name which begins with `__` (two underscores), as this is used exclusively by GraphQL’s introspection system.
* The type of an object field argument must be an input type (any type except an Object, Interface, or Union type).

#### Interface Type Definition

* Fields on a GraphQL interface have the same rules as fields on a GraphQL object; their type can be Scalar, Object, Enum, Interface, or Union, or any wrapping type whose base type is one of those five.

```
1. An Interface type must define one or more fields.
2. For each field of an Interface type:
    1. The field must have a unique name within that Interface type; no two fields may share the same name.
    2. The field must not have a name which begins with the characters "__" (two underscores).
    3. The field must return a type where IsOutputType(fieldType) returns true.
    4. For each argument of the field:
        1. The argument must not have a name which begins with the characters "__" (two underscores).
        2. The argument must accept a type where IsInputType(argumentType) returns true.
```

#### Union Type Definition

```
1. A Union type must include one or more unique member types.
2. The member types of a Union type must all be Object base types; Scalar, Interface and Union types must not be member types of a Union. Similarly, wrapping types must not be member types of a Union.
```

#### Enum Type Definition

* An Enum type must define one or more unique enum values.

#### InputObject Type Definition

```
1. An Input Object type must define one or more input fields.
2. For each input field of an Input Object type:
    1. The input field must have a unique name within that Input Object type; no two input fields may share the same name.
    2. The input field must not have a name which begins with the characters "__" (two underscores).
    3. The input field must accept a type where IsInputType(inputFieldType) returns true.
```

### Wrapping Type

#### Non-Null Type

* A Non‐Null type must not wrap another Non‐Null type.

### Directive Definition

```
1. A directive definition must not contain the use of a directive which references itself directly.
2. A directive definition must not contain the use of a directive which references itself indirectly by referencing a Type or Directive which transitively includes a reference to this directive.
3. The directive must not have a name which begins with the characters "__" (two underscores).
4. For each argument of the directive:
    1. The argument must not have a name which begins with the characters "__" (two underscores).
    2. The argument must accept a type where IsInputType(argumentType) returns true.
```

## Type System Extensions

### Schema Extension

* The Schema must already be defined.
* Any directives provided must not already apply to the original Schema.

### Type Extension

#### Scalar Type Extension

* The named type must already be defined and must be a Scalar type.
* Any directives provided must not already apply to the original Scalar type.

#### Object Type Extension

* The named type must already be defined and must be an Object type.
* The fields of an Object type extension must have unique names; no two fields may share the same name.
* Any fields of an Object type extension must not be already defined on the original Object type.
* Any directives provided must not already apply to the original Object type.
* Any interfaces provided must not be already implemented by the original Object type.
* The resulting extended object type must be a super‐set of all interfaces it implements.

#### Interface Type Extension

```
1. The named type must already be defined and must be an Interface type.
2. The fields of an Interface type extension must have unique names; no two fields may share the same name.
3. Any fields of an Interface type extension must not be already defined on the original Interface type.
4. Any Object type which implemented the original Interface type must also be a super‐set of the fields of the Interface type extension (which may be due to Object type extension).
5. Any directives provided must not already apply to the original Interface type.
```

#### Union Type Extension

```
1. The named type must already be defined and must be a Union type.
2. The member types of a Union type extension must all be Object base types; Scalar, Interface and Union types must not be member types of a Union. Similarly, wrapping types must not be member types of a Union.
3. All member types of a Union type extension must be unique.
4. All member types of a Union type extension must not already be a member of the original Union type.
5. Any directives provided must not already apply to the original Union type.
```

#### Enum Type Extension

```
1. The named type must already be defined and must be an Enum type.
2. All values of an Enum type extension must be unique.
3. All values of an Enum type extension must not already be a value of the original Enum.
4. Any directives provided must not already apply to the original Enum type.
```

#### InputObject Type Extension

```
1. The named type must already be defined and must be a Input Object type.
2. All fields of an Input Object type extension must have unique names.
3. All fields of an Input Object type extension must not already be a field of the original Input Object.
4. Any directives provided must not already apply to the original Input Object type.
```

## Misc

### Reserved Names

Types and fields required by the GraphQL introspection system that are used in the same context as user‐defined types and fields are prefixed with `__` two underscores. This in order to avoid naming collisions with user‐defined GraphQL types. Conversely, GraphQL type system authors must not define any types, fields, arguments, or any other type system artifact with two leading underscores.
