import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import ValidEnumDefinitionsRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            enum Foo {
              BAR
              BAZ
            }
            """,
            [],
        ),
        (
            """
            enum __Foo {
              BAR
              BAZ
            }
            """,
            [
                TartifletteError(
                    message='Name < __Foo > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=2, column=18, line_end=2, column_end=23)
                    ],
                )
            ],
        ),
        (
            """
            enum Foo {
              __BAR
              __BAZ
            }
            """,
            [
                TartifletteError(
                    message='Name < __BAR > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=20)
                    ],
                ),
                TartifletteError(
                    message='Name < __BAZ > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=20)
                    ],
                ),
            ],
        ),
    ],
)
async def test_valid_enum_definitions(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[ValidEnumDefinitionsRule])
        == expected
    )
