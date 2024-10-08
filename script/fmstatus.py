import requests
import os
from datetime import datetime
from termcolor import colored

# Replace this with your personal API-key for LastFM.
API_KEY = '000000000000000000000000000'

def fetch_user_info(username):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'user.getinfo',
        'user': username,
        'api_key': API_KEY,
        'format': 'json'
    }
    response = requests.get(url, params=params)
    return response.json()

def fetch_recent_tracks(username, limit=2):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'user.getrecenttracks',
        'user': username,
        'api_key': API_KEY,
        'format': 'json',
        'limit': limit
    }
    response = requests.get(url, params=params)
    return response.json()

def calculate_total_time_spent(username):
    url = 'http://ws.audioscrobbler.com/2.0/'
    limit = 1000
    total_seconds = 0
    page = 1

    while True:
        params = {
            'method': 'user.gettoptracks',
            'user': username,
            'api_key': API_KEY,
            'format': 'json',
            'limit': limit,
            'page': page
        }
        response = requests.get(url, params=params)
        top_tracks = response.json().get('toptracks', {}).get('track', [])

        if not top_tracks:
            break

        for track in top_tracks:
            playcount = int(track.get('playcount', 0))
            duration = int(track.get('duration', 0))
            total_seconds += playcount * duration

        page += 1

    return total_seconds

def seconds_to_pretty_time(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    total_hours = days * 24 + hours
    return f"{days} Days {hours} Hours {minutes} Minutes {seconds} Seconds ({total_hours} Hours)"

def format_timestamp(timestamp):
    dt = datetime.fromtimestamp(int(timestamp))
    local_time = dt.strftime('%d/%m/%Y %H:%M %Z')
    return local_time

def display_user_stats(user_info, recent_tracks, total_time_spent):
    user = user_info.get('user', {})

    os.system('cls' if os.name == 'nt' else 'clear')

    username = user.get('name', 'Unknown')
    playcount = f"{int(user.get('playcount', '0')):,}"
    country = user.get('country', 'N/A')
    registered = format_timestamp(user.get('registered', {}).get('unixtime', 'N/A'))

    recent_tracks_list = recent_tracks.get('recenttracks', {}).get('track', [])
    current_track = recent_tracks_list[0] if len(recent_tracks_list) > 0 else {}
    last_track = recent_tracks_list[1] if len(recent_tracks_list) > 1 else {}

    current_track_name = current_track.get('name', 'N/A')
    current_artist_name = current_track.get('artist', {}).get('#text', 'N/A')

    last_track_name = last_track.get('name', 'N/A')
    last_artist_name = last_track.get('artist', {}).get('#text', 'N/A')

    print(colored(f"Username: ", 'yellow') + colored(username, 'white'))
    print(colored(f"Country: ", 'yellow') + colored(country, 'white'))
    print(colored(f"Registered: ", 'yellow') + colored(registered, 'white'))
    print(colored(f"Playcount: ", 'yellow') + colored(playcount, 'white'))
    print(colored(f"Currently playing: ", 'yellow') + colored(f"{current_track_name} by {current_artist_name}", 'white'))
    print(colored(f"Last played: ", 'yellow') + colored(f"{last_track_name} by {last_artist_name}", 'white'))
    print(colored(f"Total time spent listening: ", 'yellow') + colored(seconds_to_pretty_time(total_time_spent), 'white'))

def main():
    username = input(colored("Provide username >>> ", 'yellow')).strip()
    print(colored("Fetching user information...", 'yellow'))
    
    user_info = fetch_user_info(username)
    recent_tracks = fetch_recent_tracks(username)
    total_time_spent = calculate_total_time_spent(username)
    
    display_user_stats(user_info, recent_tracks, total_time_spent)

if __name__ == "__main__":
    main()
