"""Tests for schema enum message.category.symbol.000"""
from gnf.enums import MessageCategorySymbol


def test_message_category_symbol():

    assert set(MessageCategorySymbol.values()) == {
        "unknown",
        "rj",
        "rjb",
        "s",
        "mq",
        "post",
        "postack",
        "get",
    }

    assert MessageCategorySymbol.default() == MessageCategorySymbol.unknown
