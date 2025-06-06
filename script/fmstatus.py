import requests
from datetime import datetime
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

API_KEY = '6C6F7665'
API_URL = 'https://ws.audioscrobbler.com/2.0/'

console = Console()


def fetch_user_info(username: str) -> dict:
    response = requests.get(API_URL, params={
        'method': 'user.getinfo',
        'user': username,
        'api_key': API_KEY,
        'format': 'json'
    })
    return response.json()


def fetch_recent_tracks(username: str, limit: int = 2) -> dict:
    response = requests.get(API_URL, params={
        'method': 'user.getrecenttracks',
        'user': username,
        'api_key': API_KEY,
        'format': 'json',
        'limit': limit
    })
    return response.json()


def calculate_total_time_spent(username: str) -> int:
    total_seconds, page, limit = 0, 1, 1000

    while True:
        response = requests.get(API_URL, params={
            'method': 'user.gettoptracks',
            'user': username,
            'api_key': API_KEY,
            'format': 'json',
            'limit': limit,
            'page': page
        })
        tracks = response.json().get('toptracks', {}).get('track', [])
        if not tracks:
            break

        for track in tracks:
            playcount = int(track.get('playcount', 0))
            duration = int(track.get('duration', 0))
            total_seconds += playcount * duration

        page += 1

    return total_seconds


def seconds_to_pretty_time(seconds: int) -> str:
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    total_hours = days * 24 + hours
    return f"{days}d {hours}h {minutes}m {seconds}s ({total_hours}h)"


def format_timestamp(timestamp: str) -> str:
    try:
        dt = datetime.fromtimestamp(int(timestamp))
        return dt.strftime('%d/%m/%Y %H:%M')
    except:
        return "N/A"


def display_user_stats(user_info: dict, recent_tracks: dict, total_time: int):
    user = user_info.get('user', {})

    username = user.get('name', 'Unknown')
    playcount = f"{int(user.get('playcount', '0')):,}"
    country = user.get('country', 'N/A')
    registered = format_timestamp(user.get('registered', {}).get('unixtime', '0'))

    recent = recent_tracks.get('recenttracks', {}).get('track', [])
    now_playing = recent[0] if len(recent) > 0 else {}
    last_played = recent[1] if len(recent) > 1 else {}

    now_title = now_playing.get('name', 'N/A')
    now_artist = now_playing.get('artist', {}).get('#text', 'N/A')

    last_title = last_played.get('name', 'N/A')
    last_artist = last_played.get('artist', {}).get('#text', 'N/A')

    table = Table(title="🎵 Last.fm User Stats", header_style="bold cyan")
    table.add_column("Field", style="bold")
    table.add_column("Value")

    table.add_row("Username", username)
    table.add_row("Country", country)
    table.add_row("Registered", registered)
    table.add_row("Playcount", playcount)
    table.add_row("Now Playing", f"{now_title} — {now_artist}")
    table.add_row("Last Played", f"{last_title} — {last_artist}")
    table.add_row("Total Time Listening", seconds_to_pretty_time(total_time))

    console.clear()
    console.print(Panel(table, border_style="bright_blue"))


def main():
    username = Prompt.ask("[bold magenta]Enter Last.fm username[/]")
    console.print("[italic cyan]Fetching data...[/]")

    try:
        user_info = fetch_user_info(username)
        recent_tracks = fetch_recent_tracks(username)
        total_time = calculate_total_time_spent(username)
        display_user_stats(user_info, recent_tracks, total_time)
    except Exception as e:
        console.print(f"[bold red]Error:[/] {e}")


if __name__ == "__main__":
    main()
