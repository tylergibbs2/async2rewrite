import async2rewrite


def test_is_default():
    converted_code = async2rewrite.from_text("role.is_default")
    assert converted_code == "role.is_default()"


def test_is_ready():
    converted_code = async2rewrite.from_text("bot.is_ready")
    assert converted_code == "bot.is_ready()"


def test_is_closed():
    converted_code = async2rewrite.from_text("bot.is_closed")
    assert converted_code == "bot.is_closed()"
