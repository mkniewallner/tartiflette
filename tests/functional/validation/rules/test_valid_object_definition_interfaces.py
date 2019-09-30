import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import ValidObjectDefinitionInterfacesRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            scalar Int

            interface Bar {
              barField: [Int!]
            }

            interface Baz {
              bazField: Int!
            }

            type Foo implements Bar & Baz {
              barField: [Int!]
              bazField: Int!
            }
            """,
            [],
        )
    ],
)
async def test_valid_object_definition_interfaces(sdl, expected):
    assert (
        validate_sdl(
            parse_to_document(sdl), rules=[ValidObjectDefinitionInterfacesRule]
        )
        == expected
    )
