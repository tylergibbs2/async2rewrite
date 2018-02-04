import async2rewrite
import pytest

import warnings


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


def test_get_bans():
    converted_code = async2rewrite.from_text("bot.get_bans(guild)")
    assert converted_code == "guild.bans()"


def test_get_message():
    converted_code = async2rewrite.from_text("bot.get_message(channel, id)")
    assert converted_code == "channel.get_message(id)"


def test_get_reaction_users():
    converted_code = async2rewrite.from_text("bot.get_reaction_users(rxn, limit=10)")
    assert converted_code == "rxn.users(limit=10)"


def test_invites_from():
    converted_code = async2rewrite.from_text("bot.invites_from(server=guild)")
    assert converted_code == "guild.invites()"


def test_kick():
    converted_code = async2rewrite.from_text("bot.kick(member)")
    assert converted_code == "member.kick()"


def test_leave_server():
    converted_code = async2rewrite.from_text("bot.leave_server(server)")
    assert converted_code == "guild.leave()"


def test_logs_from():
    converted_code = async2rewrite.from_text("bot.logs_from(chan, limit=50, reverse=True)")
    assert converted_code == "chan.history(limit=50, reverse=True)"


def test_move_channel():
    converted_code = async2rewrite.from_text("bot.move_channel(channel, position)")
    assert converted_code == "channel.edit(position=position)"


def test_move_role():
    converted_code = async2rewrite.from_text("bot.move_role(server, role, pos)")
    assert converted_code == "role.edit(position=pos)"


def test_move_member():
    converted_code = async2rewrite.from_text("bot.move_member(mem, chan)")
    assert converted_code == "mem.edit(voice_channel=chan)"


def test_pin_message():
    converted_code = async2rewrite.from_text("bot.pin_message(msg)")
    assert converted_code == "msg.pin()"


def test_pins_from():
    converted_code = async2rewrite.from_text("bot.pins_from(dest)")
    assert converted_code == "dest.pins()"


def test_prune_members():
    converted_code = async2rewrite.from_text("bot.prune_members(server)")
    assert converted_code == "guild.prune_members()"


def test_purge_from():
    converted_code = async2rewrite.from_text("bot.purge_from(dest, limit=5, check=my_check)")
    assert converted_code == "dest.purge(limit=5, check=my_check)"


def test_remove_reaction():
    converted_code = async2rewrite.from_text("bot.remove_reaction(msg, emoji, member)")
    assert converted_code == "msg.remove_reaction(emoji, member)"


def test_remove_roles():
    converted_code = async2rewrite.from_text("bot.remove_roles(member, role1, role2, role3)")
    assert converted_code == "member.remove_roles(role1, role2, role3)"


def test_replace_roles():
    converted_code = async2rewrite.from_text("bot.replace_roles(member, role1, role2)")
    assert converted_code == "member.edit(roles=[role1, role2])"


def test_send_file():
    converted_code = async2rewrite.from_text("bot.send_file(dest, 'to_send.png',"
                                             " filename='my_file.png', content='File')")
    assert converted_code == "dest.send('File', file=discord.File('to_send.png', filename='my_file.png'))"


def test_send_message():
    converted_code = async2rewrite.from_text("bot.send_message(dest, 'Content')")
    assert converted_code == "dest.send('Content')"


def test_send_typing():
    converted_code = async2rewrite.from_text("bot.send_typing(dest)")
    assert converted_code == "dest.trigger_typing()"


def test_server_voice_state():
    converted_code = async2rewrite.from_text("bot.server_voice_state(member, mute=True, deafen=True)")
    assert converted_code == "member.edit(mute=True, deafen=True)"


def test_stateful_start_private_message():
    converted_code = async2rewrite.from_text("bot.start_private_message(user)")
    assert converted_code == "user.create_dm()"


def test_unban():
    converted_code = async2rewrite.from_text("bot.unban(server, user)")
    assert converted_code == "guild.unban(user)"


def test_unpin_message():
    converted_code = async2rewrite.from_text("bot.unpin_message(msg)")
    assert converted_code == "msg.unpin()"


def test_wait_for_message_working():
    converted_code = async2rewrite.from_text("bot.wait_for_message(check=my_check)")
    assert converted_code == "bot.wait_for('message', check=my_check)"


def test_wait_for_message_warning():
    with pytest.warns(UserWarning):
        async2rewrite.from_text("bot.wait_for_message(author=member)")


def test_wait_for_reaction_working():
    converted_code = async2rewrite.from_text("bot.wait_for_reaction(check=my_check)")
    assert converted_code == "bot.wait_for('reaction_add', check=my_check)"


def test_wait_for_reaction_warning():
    with pytest.warns(UserWarning):
        async2rewrite.from_text("bot.wait_for_reaction(author=member)")
