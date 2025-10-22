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
    """Return the percentage of achievements unlocked for a game.
    Returns:
        -1 if the game has no achievements,
        0-100 for the unlocked percentage.
    """
    url = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/"
    params = {"key": api_key, "steamid": steam_id, "appid": appid}
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return "N/A"

    data = r.json().get("playerstats", {})

    achievements = data.get("achievements")
    if achievements is None:
        # No achievements exist to unlock
        return -1

    total = len(achievements)
    if total == 0:
        return -1

    unlocked = sum(1 for a in achievements if a.get("achieved", 0) == 1)
    percentage = round((unlocked / total) * 100, 1)
    return percentage


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

    output_lines = ["TITLE, HOURS PLAYED, PERCENTAGE ACHIEVEMENTS, DATE LAST PLAYED"]

    for game in games:
        name = game.get("name", "Unknown").replace(",", ":")  # replace commas in titles
        hours_played = round(game.get("playtime_forever", 0) / 60, 1)
        last_played = get_last_played(game.get("rtime_last_played", 0))

        # Skip games with no playtime and no last played date
        if hours_played == 0 and last_played == "Never":
            continue

        # Get achievement percentage
        achievement_percentage = get_achievement_percentage(api_key, steam_id, game["appid"])

        # Skip games with 0% achievements unless >=10 hours
        if isinstance(achievement_percentage, (int, float)) and achievement_percentage == 0 and hours_played < 10:
            continue

        # Skip games with less than 5 hours played
        if hours_played < 5:
            continue

        # Format achievement string
        if isinstance(achievement_percentage, (int, float)):
            if achievement_percentage == -1:
                achievement_str = "N/A"  # no achievements exist
            else:
                achievement_str = f"{achievement_percentage:.1f}%"
        else:
            achievement_str = "N/A"

        line = f"{name}, {hours_played}, {achievement_str}, {last_played}"
        output_lines.append(line)
        print(line)

    # Write to file
    with open("steam_game_list.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    print("\nSaved as 'steam_game_list.txt'")


if __name__ == "__main__":
    main()
