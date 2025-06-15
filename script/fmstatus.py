import requests
from datetime import datetime
from rich import print
from rich.console import Console
from rich.text import Text
from rich.style import Style
from rich.prompt import Prompt

API_KEY = '777'
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
    avg_track_length = 210
    
    while True:
        response = requests.get(API_URL, params={
            'method': 'user.gettoptracks',
            'user': username,
            'api_key': API_KEY,
            'format': 'json',
            'limit': limit,
            'page': page
        })
        data = response.json()
        tracks = data.get('toptracks', {}).get('track', [])
        if not tracks:
            break

        for track in tracks:
            playcount = int(track.get('playcount', 0))
            duration = int(track.get('duration', 0))
            if duration <= 0:
                duration = avg_track_length
            total_seconds += playcount * duration

        page += 1
    return total_seconds

def seconds_to_pretty_time(seconds: int) -> str:
    if seconds < 1:
        return "Not enough data"
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
    recent = recent_tracks.get('recenttracks', {}).get('track', [])
    
    username = user.get('name', 'Unknown')
    playcount = f"{int(user.get('playcount', '0')):,}"
    country = user.get('country', 'N/A')
    registered = format_timestamp(user.get('registered', {}).get('unixtime', '0'))
    
    now_playing = recent[0] if recent else {}
    last_played = recent[1] if len(recent) > 1 else {}
    
    now_title = now_playing.get('name', 'Nothing playing')
    now_artist = now_playing.get('artist', {}).get('#text', '')
    last_title = last_played.get('name', 'None yet')
    last_artist = last_played.get('artist', {}).get('#text', '')
    
    time_pretty = seconds_to_pretty_time(total_time)
    
    console.clear()
    console.print(
        Text("🌸  Last.fm User Stats  🌸", 
             style=Style(color="#ff9ff3", bold=True, italic=True)),
        justify="center"
    )
    console.print()
    
    console.print(
        Text("👤 Username: ", style="#feca57") + 
        Text(username, style="#ff9ff3 bold")
    )
    console.print(
        Text("🌍 Country: ", style="#feca57") + 
        Text(country, style="#ff9ff3")
    )
    console.print(
        Text("📅 Registered: ", style="#feca57") + 
        Text(registered, style="#ff9ff3")
    )
    console.print(
        Text("🎵 Total Plays: ", style="#feca57") + 
        Text(playcount, style="#ff9ff3 bold")
    )
    console.print()
    
    console.print(
        Text("🎶 Now Playing: ", style="#1dd1a1 bold") +
        Text(f"{now_title}", style="#f368e0") +
        Text(" — ", style="#c8d6e5") +
        Text(now_artist, style="#ff9ff3 italic")
    )
    
    console.print(
        Text("⏮ Last Played: ", style="#1dd1a1") +
        Text(f"{last_title}", style="#f368e0") +
        Text(" — ", style="#c8d6e5") +
        Text(last_artist, style="#ff9ff3 italic")
    )
    console.print()
    
    console.print(
        Text("⏳ Total Listening Time: ", style="#feca57 bold") +
        Text(time_pretty, style="#5f27cd bold")
    )
    
    console.print()
    console.print(
        Text("✨ Powered by Last.fm & Python ✨", 
             style=Style(color="#c8d6e5", italic=True)),
        justify="center"
    )

def main():
    username = Prompt.ask("[bold #f368e0]Enter Last.fm username[/]")
    console.print("[italic #1dd1a1]Fetching data...[/]")

    try:
        user_info = fetch_user_info(username)
        recent_tracks = fetch_recent_tracks(username)
        total_time = calculate_total_time_spent(username)
        display_user_stats(user_info, recent_tracks, total_time)
    except Exception as e:
        console.print(f"[bold red]Error:[/] {e}")

if __name__ == "__main__":
    main()
