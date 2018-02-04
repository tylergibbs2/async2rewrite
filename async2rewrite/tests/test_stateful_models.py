import async2rewrite


def test_add_reaction():
    converted_code = async2rewrite.from_text("bot.add_reaction(msg, rxn)")
    assert converted_code == "msg.add_reaction(rxn)"


def test_add_roles():
    converted_code = async2rewrite.from_text("bot.add_roles(member, role1, role2, role3)")
    assert converted_code == "member.add_roles(role1, role2, role3)"


def test_ban():
    converted_code = async2rewrite.from_text("bot.ban(member)")
    assert converted_code == "member.ban()"


def test_change_nickname():
    converted_code = async2rewrite.from_text("bot.change_nickname(member, 'New Nick')")
    assert converted_code == "member.edit(nick='New Nick')"


def test_clear_reactions():
    converted_code = async2rewrite.from_text("bot.clear_reactions(msg)")
    assert converted_code == "msg.clear_reactions()"


def test_create_custom_emoji():
    converted_code = async2rewrite.from_text("bot.create_custom_emoji(server, name='Name', image=img_obj)")
    assert converted_code == "guild.create_custom_emoji(name='Name', image=img_obj)"


def test_create_text_channel():
    converted_code = async2rewrite.from_text("bot.create_channel(server, 'Text', type=discord.ChannelType.text)")
    assert converted_code == "guild.create_text_channel('Text')"


def test_create_voice_channel():
    converted_code = async2rewrite.from_text("bot.create_channel(server, 'Voice', type=discord.ChannelType.voice)")
    assert converted_code == "guild.create_voice_channel('Voice')"


def test_create_invite():
    converted_code = async2rewrite.from_text("bot.create_invite(destination, max_age=10, max_uses=3)")
    assert converted_code == "destination.create_invite(max_age=10, max_uses=3)"


def test_create_role():
    converted_code = async2rewrite.from_text("bot.create_role(server, name='New Role', hoist=True)")
    assert converted_code == "guild.create_role(name='New Role', hoist=True)"


def test_delete_channel():
    converted_code = async2rewrite.from_text("bot.delete_channel(channel)")
    assert converted_code == "channel.delete()"


def test_delete_channel_perms():
    converted_code = async2rewrite.from_text("bot.delete_channel_permissions(channel)")
    assert converted_code == "channel.set_permissions(overwrite=None)"


def test_delete_custom_emoji():
    converted_code = async2rewrite.from_text("bot.delete_custom_emoji(emoji)")
    assert converted_code == "emoji.delete()"


def test_delete_invite():
    converted_code = async2rewrite.from_text("bot.delete_invite(inv)")
    assert converted_code == "inv.delete()"


def test_delete_message():
    converted_code = async2rewrite.from_text("bot.delete_message(msg)")
    assert converted_code == "msg.delete()"


def test_delete_role():
    converted_code = async2rewrite.from_text("bot.delete_role(server, role)")
    assert converted_code == "role.delete()"


def test_delete_server():
    converted_code = async2rewrite.from_text("bot.delete_server(server)")
    assert converted_code == "guild.delete()"


def test_edit_channel():
    converted_code = async2rewrite.from_text("bot.edit_channel(channel, topic='GG', user_limit=10)")
    assert converted_code == "channel.edit(topic='GG', user_limit=10)"


def test_edit_channel_permissions():
    converted_code = async2rewrite.from_text("bot.edit_channel_permissions(channel, target, overwrite=some_overwrite)")
    assert converted_code == "channel.set_permissions(target, overwrite=some_overwrite)"


def test_edit_custom_emoji():
    converted_code = async2rewrite.from_text("bot.edit_custom_emoji(emoji, name='Test')")
    assert converted_code == "emoji.edit(name='Test')"


def test_edit_message():
    converted_code = async2rewrite.from_text("bot.edit_message(msg, 'New Content', embed=new_embed)")
    assert converted_code == "msg.edit(embed=new_embed, content='New Content')"


def test_edit_profile():
    converted_code = async2rewrite.from_text("bot.edit_profile(username='New Username')")
    assert converted_code == "bot.user.edit(username='New Username')"


def test_edit_role():
    converted_code = async2rewrite.from_text("bot.edit_role(server, role, name='New Name')")
    assert converted_code == "role.edit(name='New Name')"


def test_edit_server():
    converted_code = async2rewrite.from_text("bot.edit_server(server, name='New Name')")
    assert converted_code == "guild.edit(name='New Name')"


def test_estimate_pruned_members():
    converted_code = async2rewrite.from_text("bot.estimate_pruned_members(location)")
    assert converted_code == "location.estimate_pruned_members()"


def test_get_all_emojis():
    converted_code = async2rewrite.from_text("bot.get_all_emojis()")
    assert converted_code == "bot.emojis"
