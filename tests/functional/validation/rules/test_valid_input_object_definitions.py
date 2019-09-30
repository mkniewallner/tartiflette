import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import ValidInputObjectDefinitionsRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            scalar String
            enum Qux {
              BAR
              FOO
            }
            input Foo {
              fieldA: String
              fieldB: [Qux]
              fieldC: [String!]
              fieldD: [Qux!]!
            }
            """,
            [],
        ),
        (
            """
            input __Foo
            """,
            [
                TartifletteError(
                    message='Name < __Foo > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=2, column=19, line_end=2, column_end=24)
                    ],
                )
            ],
        ),
        (
            """
            scalar String
            input Foo {
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
                    message="Input object type < Foo > can only include field fieldA once.",
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=21),
                        Location(line=7, column=15, line_end=7, column_end=21),
                    ],
                ),
                TartifletteError(
                    message="Input object type < Foo > can only include field fieldB once.",
                    locations=[
                        Location(line=5, column=15, line_end=5, column_end=21),
                        Location(line=8, column=15, line_end=8, column_end=21),
                    ],
                ),
                TartifletteError(
                    message="Input object type < Foo > can only include field fieldA once.",
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
            input Foo {
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
            type Bar
            input Foo {
              field: Bar
            }
            """,
            [
                TartifletteError(
                    message="The type of < Foo.field > must be Input type but got: Bar.",
                    locations=[
                        Location(line=4, column=22, line_end=4, column_end=25)
                    ],
                )
            ],
        ),
        (
            """
            type Bar
            union Baz = Bar
            input Foo {
              field: [Baz!]!
            }
            """,
            [
                TartifletteError(
                    message="The type of < Foo.field > must be Input type but got: [Baz!]!.",
                    locations=[
                        Location(line=5, column=22, line_end=5, column_end=29)
                    ],
                )
            ],
        ),
        (
            """
            input Foo {
              field: Unknown
            }
            """,
            [
                TartifletteError(
                    message="The type of < Foo.field > must be Input type but got: Unknown.",
                    locations=[
                        Location(line=3, column=22, line_end=3, column_end=29)
                    ],
                )
            ],
        ),
        (
            """
            input Foo {
              field: [Unknown!]!
            }
            """,
            [
                TartifletteError(
                    message="The type of < Foo.field > must be Input type but got: [Unknown!]!.",
                    locations=[
                        Location(line=3, column=22, line_end=3, column_end=33)
                    ],
                )
            ],
        ),
    ],
)
async def test_valid_input_object_definitions(sdl, expected):
    assert (
        validate_sdl(
            parse_to_document(sdl), rules=[ValidInputObjectDefinitionsRule]
        )
        == expected
    )
