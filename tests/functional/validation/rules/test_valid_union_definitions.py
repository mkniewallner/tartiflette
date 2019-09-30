import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import ValidUnionDefinitionsRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            type Foo
            type Bar
            union Baz = Foo | Bar
            """,
            [],
        ),
        (
            """
            type Foo
            type Bar
            union __Baz = Foo | Bar
            """,
            [
                TartifletteError(
                    message='Name < __Baz > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=4, column=19, line_end=4, column_end=24)
                    ],
                )
            ],
        ),
        (
            """
            type Foo
            union Baz = Foo | Foo
            """,
            [
                TartifletteError(
                    message="Union type < Baz > can only include type Foo once.",
                    locations=[
                        Location(line=3, column=25, line_end=3, column_end=28),
                        Location(line=3, column=31, line_end=3, column_end=34),
                    ],
                )
            ],
        ),
        (
            """
            type Foo
            type Bar
            type Qux
            union Baz = Foo | Bar | Qux | Bar | Foo
            """,
            [
                TartifletteError(
                    message="Union type < Baz > can only include type Bar once.",
                    locations=[
                        Location(line=5, column=31, line_end=5, column_end=34),
                        Location(line=5, column=43, line_end=5, column_end=46),
                    ],
                ),
                TartifletteError(
                    message="Union type < Baz > can only include type Foo once.",
                    locations=[
                        Location(line=5, column=25, line_end=5, column_end=28),
                        Location(line=5, column=49, line_end=5, column_end=52),
                    ],
                ),
            ],
        ),
        (
            """
            input Foo
            union Baz = Foo
            """,
            [
                TartifletteError(
                    message="Union type < Baz > can only include Object types, it cannot include < Foo >.",
                    locations=[
                        Location(line=3, column=25, line_end=3, column_end=28)
                    ],
                )
            ],
        ),
        (
            """
            interface Foo
            union Baz = Foo
            """,
            [
                TartifletteError(
                    message="Union type < Baz > can only include Object types, it cannot include < Foo >.",
                    locations=[
                        Location(line=3, column=25, line_end=3, column_end=28)
                    ],
                )
            ],
        ),
        (
            """
            union Baz = Unknown
            """,
            [
                TartifletteError(
                    message="Union type < Baz > can only include Object types, it cannot include < Unknown >.",
                    locations=[
                        Location(line=2, column=25, line_end=2, column_end=32)
                    ],
                )
            ],
        ),
    ],
)
async def test_valid_union_definitions(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[ValidUnionDefinitionsRule])
        == expected
    )
