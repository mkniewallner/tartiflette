import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import ValidInterfaceDefinitionsRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            scalar String
            interface Bar
            type Baz
            enum Qux {
              BAR
              FOO
            }
            interface Foo {
              fieldA: String
              fieldB: [Bar]
              fieldC: [Baz!]
              fieldD: [Qux!]!
            }
            """,
            [],
        ),
        (
            """
            interface __Foo
            """,
            [
                TartifletteError(
                    message='Name < __Foo > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=2, column=23, line_end=2, column_end=28)
                    ],
                )
            ],
        ),
        (
            """
            scalar String
            interface Foo {
              fieldA: String
              fieldB: String
              fieldC: String
              fieldA: String
              fieldB: String
              fieldA: String
            }
            """,
            [
                TartifletteError(
                    message="Interface type < Foo > can only include field fieldA once.",
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=21),
                        Location(line=7, column=15, line_end=7, column_end=21),
                    ],
                ),
                TartifletteError(
                    message="Interface type < Foo > can only include field fieldB once.",
                    locations=[
                        Location(line=5, column=15, line_end=5, column_end=21),
                        Location(line=8, column=15, line_end=8, column_end=21),
                    ],
                ),
                TartifletteError(
                    message="Interface type < Foo > can only include field fieldA once.",
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=21),
                        Location(line=9, column=15, line_end=9, column_end=21),
                    ],
                ),
            ],
        ),
        (
            """
            scalar String
            interface Foo {
              __fieldA: String
              __fieldB: String
            }
            """,
            [
                TartifletteError(
                    message='Name < __fieldA > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=23)
                    ],
                ),
                TartifletteError(
                    message='Name < __fieldB > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=5, column=15, line_end=5, column_end=23)
                    ],
                ),
            ],
        ),
        (
            """
            input Bar
            interface Foo {
              field: Bar
            }
            """,
            [
                TartifletteError(
                    message="The type of < Foo.field > must be Output type but got: Bar.",
                    locations=[
                        Location(line=4, column=22, line_end=4, column_end=25)
                    ],
                )
            ],
        ),
        (
            """
            input Bar
            interface Foo {
              field: [Bar!]!
            }
            """,
            [
                TartifletteError(
                    message="The type of < Foo.field > must be Output type but got: [Bar!]!.",
                    locations=[
                        Location(line=4, column=22, line_end=4, column_end=29)
                    ],
                )
            ],
        ),
        (
            """
            interface Foo {
              field: Unknown
            }
            """,
            [
                TartifletteError(
                    message="The type of < Foo.field > must be Output type but got: Unknown.",
                    locations=[
                        Location(line=3, column=22, line_end=3, column_end=29)
                    ],
                )
            ],
        ),
        (
            """
            interface Foo {
              field: [Unknown!]!
            }
            """,
            [
                TartifletteError(
                    message="The type of < Foo.field > must be Output type but got: [Unknown!]!.",
                    locations=[
                        Location(line=3, column=22, line_end=3, column_end=33)
                    ],
                )
            ],
        ),
        (
            """
            scalar String
            interface Foo {
              field(arg1: String, arg2: String): String
            }
            """,
            [],
        ),
        (
            """
            scalar String
            interface Foo {
              field(
                arg1: String
                arg2: String
                arg3: String
                arg1: String
                arg2: String
              ): String
            }
            """,
            [
                TartifletteError(
                    message="Field argument < Foo.field(arg1) > can only be defined once.",
                    locations=[
                        Location(line=5, column=17, line_end=5, column_end=21),
                        Location(line=8, column=17, line_end=8, column_end=21),
                    ],
                ),
                TartifletteError(
                    message="Field argument < Foo.field(arg2) > can only be defined once.",
                    locations=[
                        Location(line=6, column=17, line_end=6, column_end=21),
                        Location(line=9, column=17, line_end=9, column_end=21),
                    ],
                ),
            ],
        ),
        (
            """
            scalar String
            interface Foo {
              field(
                __arg1: String
                __arg2: String
              ): String
            }
            """,
            [
                TartifletteError(
                    message='Name < __arg1 > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=5, column=17, line_end=5, column_end=23)
                    ],
                ),
                TartifletteError(
                    message='Name < __arg2 > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=6, column=17, line_end=6, column_end=23)
                    ],
                ),
            ],
        ),
        (
            """
            type Bar
            union Baz = Bar
            scalar String
            interface Foo {
              fieldA(arg: Bar): String
              fieldB(arg: [Baz!]!): String
            }
            """,
            [
                TartifletteError(
                    message="The type of < Foo.fieldA(arg) > must be Input type but got: Bar.",
                    locations=[
                        Location(line=6, column=27, line_end=6, column_end=30)
                    ],
                ),
                TartifletteError(
                    message="The type of < Foo.fieldB(arg) > must be Input type but got: [Baz!]!.",
                    locations=[
                        Location(line=7, column=27, line_end=7, column_end=34)
                    ],
                ),
            ],
        ),
    ],
)
async def test_valid_interface_definitions(sdl, expected):
    assert (
        validate_sdl(
            parse_to_document(sdl), rules=[ValidInterfaceDefinitionsRule]
        )
        == expected
    )
