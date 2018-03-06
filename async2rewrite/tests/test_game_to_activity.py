import async2rewrite


def test_change_presence_activity_keyword():
    converted_code = async2rewrite.from_text("client.change_presence(game=discord.Game(name='a game'))")
    assert converted_code == "client.change_presence(activity=discord.Game(name='a game'))"


def test_game_type_1_to_streaming():
    converted_code = async2rewrite.from_text("client.change_presence(game=discord.Game("
                                             "name='Streaming', url=my_url, type=1))")
    assert converted_code == "client.change_presence(activity=discord.Streaming(name='Streaming', url=my_url))"


def test_game_type_2_to_activity():
    converted_code = async2rewrite.from_text("client.change_presence(game=discord.Game(name='music', type=2))")
    assert converted_code == "client.change_presence(activity=discord.Activity(" \
                             "type=discord.ActivityType.listening, name='music'))"


def test_game_type_3_to_activity():
    converted_code = async2rewrite.from_text("client.change_presence(game=discord.Game(name='a movie', type=3))")
    assert converted_code == "client.change_presence(activity=discord.Activity(" \
                             "type=discord.ActivityType.watching, name='a movie'))"


def test_member_game_to_activity():
    converted_code = async2rewrite.from_text("member.game")
    assert converted_code == "member.activity"


def test_game_to_activity_client_keywork():
    converted_code = async2rewrite.from_text("bot = discord.Bot(game=discord.Game(name='a game'))")
    assert converted_code == "bot = discord.Bot(activity=discord.Game(name='a game'))"
