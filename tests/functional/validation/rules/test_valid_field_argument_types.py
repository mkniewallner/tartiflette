import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import ValidFieldArgumentTypesRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize("kind_definition_type", ["interface", "type"])
@pytest.mark.parametrize(
    "argument_type_sdl,argument_type,expected",
    [
        ("scalar Foo", "Foo", []),
        ("scalar Foo", "Foo!", []),
        ("scalar Foo", "[Foo]", []),
        ("scalar Foo", "[Foo]!", []),
        ("scalar Foo", "[[Foo!]!]!", []),
        (
            "type Foo",
            "Foo",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: Foo.",
                    locations=[
                        Location(line=5, column=18, line_end=5, column_end=21)
                    ],
                )
            ],
        ),
        (
            "type Foo",
            "Foo!",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: Foo!.",
                    locations=[
                        Location(line=5, column=18, line_end=5, column_end=22)
                    ],
                )
            ],
        ),
        (
            "type Foo",
            "[Foo]",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: [Foo].",
                    locations=[
                        Location(line=5, column=18, line_end=5, column_end=23)
                    ],
                )
            ],
        ),
        (
            "type Foo",
            "[Foo]!",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: [Foo]!.",
                    locations=[
                        Location(line=5, column=18, line_end=5, column_end=24)
                    ],
                )
            ],
        ),
        (
            "type Foo",
            "[[Foo!]!]!",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: [[Foo!]!]!.",
                    locations=[
                        Location(line=5, column=18, line_end=5, column_end=28)
                    ],
                )
            ],
        ),
        (
            "interface Foo",
            "Foo",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: Foo.",
                    locations=[
                        Location(line=5, column=18, line_end=5, column_end=21)
                    ],
                )
            ],
        ),
        (
            "interface Foo",
            "Foo!",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: Foo!.",
                    locations=[
                        Location(line=5, column=18, line_end=5, column_end=22)
                    ],
                )
            ],
        ),
        (
            "interface Foo",
            "[Foo]",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: [Foo].",
                    locations=[
                        Location(line=5, column=18, line_end=5, column_end=23)
                    ],
                )
            ],
        ),
        (
            "interface Foo",
            "[Foo]!",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: [Foo]!.",
                    locations=[
                        Location(line=5, column=18, line_end=5, column_end=24)
                    ],
                )
            ],
        ),
        (
            "interface Foo",
            "[[Foo!]!]!",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: [[Foo!]!]!.",
                    locations=[
                        Location(line=5, column=18, line_end=5, column_end=28)
                    ],
                )
            ],
        ),
        (
            """
            type Baz
            union Foo = Baz
            """,
            "Foo",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: Foo.",
                    locations=[
                        Location(line=8, column=18, line_end=8, column_end=21)
                    ],
                )
            ],
        ),
        (
            """
            type Baz
            union Foo = Baz
            """,
            "Foo!",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: Foo!.",
                    locations=[
                        Location(line=8, column=18, line_end=8, column_end=22)
                    ],
                )
            ],
        ),
        (
            """
            type Baz
            union Foo = Baz
            """,
            "[Foo]",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: [Foo].",
                    locations=[
                        Location(line=8, column=18, line_end=8, column_end=23)
                    ],
                )
            ],
        ),
        (
            """
            type Baz
            union Foo = Baz
            """,
            "[Foo]!",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: [Foo]!.",
                    locations=[
                        Location(line=8, column=18, line_end=8, column_end=24)
                    ],
                )
            ],
        ),
        (
            """
            type Baz
            union Foo = Baz
            """,
            "[[Foo!]!]!",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: [[Foo!]!]!.",
                    locations=[
                        Location(line=8, column=18, line_end=8, column_end=28)
                    ],
                )
            ],
        ),
        ("enum Foo", "Foo", []),
        ("enum Foo", "Foo!", []),
        ("enum Foo", "[Foo]", []),
        ("enum Foo", "[Foo]!", []),
        ("enum Foo", "[[Foo!]!]!", []),
        ("input Foo", "Foo", []),
        ("input Foo", "Foo!", []),
        ("input Foo", "[Foo]", []),
        ("input Foo", "[Foo]!", []),
        ("input Foo", "[[Foo!]!]!", []),
        (
            "directive @Foo on FIELD",
            "Foo",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: Foo.",
                    locations=[
                        Location(line=5, column=18, line_end=5, column_end=21)
                    ],
                )
            ],
        ),
        (
            "directive @Foo on FIELD",
            "Foo!",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: Foo!.",
                    locations=[
                        Location(line=5, column=18, line_end=5, column_end=22)
                    ],
                )
            ],
        ),
        (
            "directive @Foo on FIELD",
            "[Foo]",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: [Foo].",
                    locations=[
                        Location(line=5, column=18, line_end=5, column_end=23)
                    ],
                )
            ],
        ),
        (
            "directive @Foo on FIELD",
            "[Foo]!",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: [Foo]!.",
                    locations=[
                        Location(line=5, column=18, line_end=5, column_end=24)
                    ],
                )
            ],
        ),
        (
            "directive @Foo on FIELD",
            "[[Foo!]!]!",
            [
                TartifletteError(
                    message="The type of < Bar.field(arg:) must be Input type but got: [[Foo!]!]!.",
                    locations=[
                        Location(line=5, column=18, line_end=5, column_end=28)
                    ],
                )
            ],
        ),
    ],
)
async def test_valid_field_argument_types(
    kind_definition_type, argument_type_sdl, argument_type, expected
):
    sdl = f"""
    scalar String
    {argument_type_sdl}
    {kind_definition_type} Bar {{
      field(arg: {argument_type}): String
    }}
    """
    assert (
        validate_sdl(
            parse_to_document(sdl), rules=[ValidFieldArgumentTypesRule]
        )
        == expected
    )
