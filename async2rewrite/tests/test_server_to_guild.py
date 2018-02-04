import async2rewrite


def test_messageserver_to_messageguild():
    converted_code = async2rewrite.from_text("message.server")
    assert converted_code == "message.guild"


def test_ctxmsgserver_to_ctxguild():
    converted_code = async2rewrite.from_text("server = ctx.message.server")
    assert converted_code == "guild = ctx.guild"


def test_createserver_to_createguild():
    converted_code = async2rewrite.from_text("bot.create_server()")
    assert converted_code == "bot.create_guild()"


def test_manageserver_to_manageguild():
    converted_code = async2rewrite.from_text("perms.manage_server")
    assert converted_code == "perms.manage_guild"
