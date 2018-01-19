import async2rewrite


def test_snowflake_to_int_in_method():
    converted_code = async2rewrite.from_text("ch = client.get_channel('84319995256905728')")
    assert converted_code == "\nch = client.get_channel(84319995256905728)\n"


def test_snowflake_to_int_in_comparison():
    converted_code = async2rewrite.from_text("if message.author.id == '80528701850124288': pass")
    assert converted_code == "\nif message.author.id == 80528701850124288:\n    pass\n"


def test_snowflake_to_int():
    converted_code = async2rewrite.from_text("'123456789012345678'")
    assert converted_code == "\n123456789012345678\n"
