import async2rewrite


def test_remove_pass_context_true():
    converted_code = async2rewrite.from_text("@bot.command(pass_context=True)\nasync def test(ctx):\n    pass")
    assert converted_code == "@bot.command()\nasync def test(ctx):\n    pass"


def test_dont_remove_pass_context_false():
    converted_code = async2rewrite.from_text("@bot.command(pass_context=False)\nasync def test():\n    pass")
    assert converted_code == "@bot.command()\nasync def test(ctx):\n    pass"


def test_say_to_send():
    converted_code = async2rewrite.from_text("bot.say('Test')")
    assert converted_code == "ctx.send('Test')"


def test_shortcut_author():
    converted_code = async2rewrite.from_text("ctx.message.author")
    assert converted_code == "ctx.author"


def test_shortcut_guild():
    converted_code = async2rewrite.from_text("ctx.message.server")
    assert converted_code == "ctx.guild"


def test_shortcut_channel():
    converted_code = async2rewrite.from_text("ctx.message.channel")
    assert converted_code == "ctx.channel"


def test_shortcut_me():
    converted_code = async2rewrite.from_text("ctx.message.server.me")
    assert converted_code == "ctx.me"
