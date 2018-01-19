import async2rewrite


def test_messageserver_to_messageguild():
    converted_code = async2rewrite.from_text("message.server")
    assert converted_code == "\nmessage.guild\n"


def test_ctxmsgserver_to_ctxguild():
    converted_code = async2rewrite.from_text("server = ctx.message.server")
    assert converted_code == "\nguild = ctx.guild\n"


def test_createserver_to_createguild():
    converted_code = async2rewrite.from_text("bot.create_server()")
    assert converted_code == "\nbot.create_guild()\n"


def test_manageserver_to_manageguild():
    converted_code = async2rewrite.from_text("perms.manage_server")
    assert converted_code == "\nperms.manage_guild\n"
