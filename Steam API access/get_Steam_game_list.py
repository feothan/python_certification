import os
import requests
from datetime import datetime

def resolve_vanity(api_key, vanity):
    """Convert Steam vanity name to 64-bit SteamID."""
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
    params = {"key": api_key, "vanityurl": vanity}
    r = requests.get(url, params=params)
    try:
        data = r.json()
    except Exception:
        raise ValueError(f"Failed to parse JSON for vanity URL '{vanity}'. Status code: {r.status_code}")
    if data.get("response", {}).get("success") != 1:
        raise ValueError(f"Could not resolve vanity '{vanity}': {data}")
    return data["response"]["steamid"]

def get_steam_games(api_key, steam_id):
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        "key": api_key,
        "steamid": steam_id,
        "include_appinfo": True,
        "include_played_free_games": True,
        "format": "json"
    }
    r = requests.get(url, params=params)
    try:
        data = r.json()
    except Exception:
        raise ValueError(f"Failed to get JSON. Response: {r.text[:200]}")
    games = data.get("response", {}).get("games", [])
    return games


def get_achievement_percentage(api_key, steam_id, appid):
    """Return % of achievements unlocked.

    If game has no achievements at all, return 100%.
    If game has achievements but none unlocked, return 0%.
    """
    url = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/"
    params = {"key": api_key, "steamid": steam_id, "appid": appid}
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return 0.0  # could not fetch

    data = r.json().get("playerstats", {})
    achievements = data.get("achievements")

    if achievements is None:
        # No achievements exist in this game
        return 100.0

    # Achievements exist, count unlocked
    total = len(achievements)
    unlocked = sum(1 for a in achievements if a.get("achieved", 0) == 1)
    return round(unlocked / total * 100, 1)


def get_last_played(epoch):
    if not epoch:
        return "Never"
    return datetime.fromtimestamp(epoch).strftime("%Y-%m-%d")

def main():
    api_key = os.getenv("STEAM_API_KEY") or input("Enter your Steam Web API key: ").strip()
    steam_input = input("Enter your 64-bit Steam ID or vanity name: ").strip()

    if not steam_input.isdigit():
        try:
            steam_id = resolve_vanity(api_key, steam_input)
            print(f"Resolved vanity '{steam_input}' to SteamID64: {steam_id}")
        except Exception as e:
            print(f"Error resolving vanity: {e}")
            return
    else:
        steam_id = steam_input

    print("\nFetching your Steam game data...")
    try:
        games = get_steam_games(api_key, steam_id)
    except Exception as e:
        print(f"Error fetching games: {e}")
        return

    if not games:
        print("No games found or profile is private.")
        return

    output_lines = []

    output_lines = []

    for game in games:
        name = game.get("name", "Unknown").replace(",", ":")
        hours_played = round(game.get("playtime_forever", 0) / 60, 1)
        last_played = get_last_played(game.get("rtime_last_played", 0))

        pct_ach = get_achievement_percentage(api_key, steam_id, game["appid"])

        line = f"{name}, {hours_played}, {pct_ach}, {last_played}"
        output_lines.append(line)
        print(line)

    with open("steam_game_list.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    print("\nSaved as 'steam_game_list.txt'")


if __name__ == "__main__":
    main()
