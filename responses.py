import os
from steam_web_api import Steam
from decouple import config

KEY = config('STEAM_API_KEY')
steam = Steam(KEY)
search_results = {}
def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return "I'm sorry, I didn't catch that. Could you repeat it?"
    elif '!help' in lowered:
        return 'Hello there!\nI am a bot that can help you find games on Steam.\n\nCommands:\n!findgame [game name] - Search for a game on Steam\n!help - Display this help message'
    elif '!findgame' in lowered:
        try:
            # Get game name from user input
            game_name = user_input.lower().split('!findgame ')[1].strip()
            print(f"Searching for game: {game_name}")
            if not game_name:
                print("No game name provided")
                return "Please provide a game name after '!findgame'."
            # Search for steam game of game_name
            game = steam.apps.search_games(str(game_name))
            print(f"Game search result: {game}")
            if game and 'apps' in game:
                game_names = [app['name'] for app in game['apps'] if 'name' in app]
                print(f"Game names: {game_names}")
                if game_names:
                    search_results['last_search'] = game['apps']
                    return "**Games found:**\n`" + "`\n`".join(game_names) + "`\nType the name of the game you want more information on."
                else:
                    return "No games found with the provided name."
            else:
                return "Game not found"
        except IndexError:
            return "Please provide a game name after '!findgame'."
    else:
        if 'last_search' in search_results:
            for app in search_results['last_search']:
                    if app['name'].lower() == lowered:
                        return f"# {app['name']}\nCurrent Price: {app['price']}\n{app['link']}\nappid: {app['id']}"
        else:
            print("No matching command found")