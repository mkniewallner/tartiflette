import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules.valid_directive_definitions import (
    ValidDirectiveDefinitionsRule,
)
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            scalar String
            scalar Int
            directive @foo(arg1: String!, arg2: [Int!]!) on FIELD
            """,
            [],
        ),
        (
            """
            directive @__foo on FIELD
            """,
            [
                TartifletteError(
                    message='Name < __foo > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=2, column=24, line_end=2, column_end=29)
                    ],
                )
            ],
        ),
        (
            """
            scalar String
            scalar Int
            directive @foo(__arg: String!) on FIELD
            """,
            [
                TartifletteError(
                    message='Name < __arg > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=4, column=28, line_end=4, column_end=33)
                    ],
                )
            ],
        ),
        (
            """
            scalar String
            scalar Int
            directive @foo(arg: String!, arg: Int!) on FIELD
            """,
            [
                TartifletteError(
                    message="Argument < @foo(arg:) > can only be defined once.",
                    locations=[
                        Location(line=4, column=28, line_end=4, column_end=31),
                        Location(line=4, column=42, line_end=4, column_end=45),
                    ],
                )
            ],
        ),
        (
            """
            scalar String
            scalar Int
            directive @foo(arg: String!, arg: Int!, arg: Int!) on FIELD
            """,
            [
                TartifletteError(
                    message="Argument < @foo(arg:) > can only be defined once.",
                    locations=[
                        Location(line=4, column=28, line_end=4, column_end=31),
                        Location(line=4, column=42, line_end=4, column_end=45),
                    ],
                ),
                TartifletteError(
                    message="Argument < @foo(arg:) > can only be defined once.",
                    locations=[
                        Location(line=4, column=28, line_end=4, column_end=31),
                        Location(line=4, column=53, line_end=4, column_end=56),
                    ],
                ),
            ],
        ),
        (
            """
            scalar String
            scalar Int
            directive @foo(
              arg1: String!
              arg2: Int!
              arg1: Int!
              arg3: Int!
              arg2: Int!
            ) on FIELD
            """,
            [
                TartifletteError(
                    message="Argument < @foo(arg1:) > can only be defined once.",
                    locations=[
                        Location(line=5, column=15, line_end=5, column_end=19),
                        Location(line=7, column=15, line_end=7, column_end=19),
                    ],
                ),
                TartifletteError(
                    message="Argument < @foo(arg2:) > can only be defined once.",
                    locations=[
                        Location(line=6, column=15, line_end=6, column_end=19),
                        Location(line=9, column=15, line_end=9, column_end=19),
                    ],
                ),
            ],
        ),
        (
            """
            directive @foo(arg: Unknown) on FIELD
            """,
            [
                TartifletteError(
                    message="The type of < @foo(arg) > must be Input type but got: Unknown.",
                    locations=[
                        Location(line=2, column=33, line_end=2, column_end=40)
                    ],
                )
            ],
        ),
        (
            """
            directive @foo(arg: Unknown!) on FIELD
            """,
            [
                TartifletteError(
                    message="The type of < @foo(arg) > must be Input type but got: Unknown!.",
                    locations=[
                        Location(line=2, column=33, line_end=2, column_end=41)
                    ],
                )
            ],
        ),
        (
            """
            type Bar
            directive @foo(arg: Bar) on FIELD
            """,
            [
                TartifletteError(
                    message="The type of < @foo(arg) > must be Input type but got: Bar.",
                    locations=[
                        Location(line=3, column=33, line_end=3, column_end=36)
                    ],
                )
            ],
        ),
        (
            """
            input Bar
            directive @foo(arg: Bar) on FIELD
            """,
            [],
        ),
    ],
)
async def test_valid_directive_definitions(sdl, expected):
    assert (
        validate_sdl(
            parse_to_document(sdl), rules=[ValidDirectiveDefinitionsRule]
        )
        == expected
    )
