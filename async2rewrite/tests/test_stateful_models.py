import async2rewrite


def test_add_reaction():
    converted_code = async2rewrite.from_text("bot.add_reaction(msg, rxn)")
    assert converted_code == "\nmsg.add_reaction(rxn)\n"


def test_add_roles():
    converted_code = async2rewrite.from_text("bot.add_roles(member, role1, role2, role3)")
    assert converted_code == "\nmember.add_roles(role1, role2, role3)\n"


def test_ban():
    converted_code = async2rewrite.from_text("bot.ban(member)")
    assert converted_code == "\nmember.ban()\n"


def test_change_nickname():
    converted_code = async2rewrite.from_text("bot.change_nickname(member, 'New Nick')")
    assert converted_code == "\nmember.edit(nick='New Nick')\n"


def test_clear_reactions():
    converted_code = async2rewrite.from_text("bot.clear_reactions(msg)")
    assert converted_code == "\nmsg.clear_reactions()\n"


def test_create_custom_emoji():
    converted_code = async2rewrite.from_text("bot.create_custom_emoji(server, name='Name', image=img_obj)")
    assert converted_code == "\nguild.create_custom_emoji(name='Name', image=img_obj)\n"


def test_create_invite():
    converted_code = async2rewrite.from_text("bot.create_channel(server, 'Name', type=discord.ChannelType.text)")
    assert converted_code == "\nguild.create_text_channel('Name')\n"
