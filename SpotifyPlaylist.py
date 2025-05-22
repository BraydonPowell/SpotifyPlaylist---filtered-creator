import spotipy
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = "client id"
CLIENT_SECRET = "client secret"
redirect_uri="redirect url"

# You can get these from the Spotify playlist URLs
SOURCE_PLAYLIST_ID = " existing playlist share link "  # the one you want to scan
TARGET_PLAYLIST_ID = "new playlist share link"  # the one to copy Drake tracks into


scope = "playlist-read-private playlist-modify-public playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=redirect_uri,
    scope=scope
))

# func to filter by artist
def get_tracks_by_artist(sp, playlist_id, artist_name):
    artist_tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    for item in tracks:
        track = item['track']
        if track and any(artist['name'].lower() == artist_name.lower() for artist in track['artists']):
            artist_tracks.append(track['uri'])

    return artist_tracks

# add track to target playlsit
def add_tracks_to_playlist(sp, playlist_id, track_uris):
    for i in range(0, len(track_uris), 100):
        sp.playlist_add_items(playlist_id, track_uris[i:i+100])


if __name__ == "__main__":
    artist_name = input("Enter the artist name to filter by: ")

    print(f" Searching for tracks by '{artist_name}' in the source playlist...")
    artist_tracks = get_tracks_by_artist(sp, SOURCE_PLAYLIST_ID, artist_name)

    if artist_tracks:
        add_tracks_to_playlist(sp, TARGET_PLAYLIST_ID, artist_tracks)
        print(f" Added {len(artist_tracks)} tracks by '{artist_name}' to the target playlist.")
    else:
        print(f" No tracks by '{artist_name}' found in the source playlist.")
