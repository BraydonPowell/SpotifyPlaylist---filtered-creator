import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ======== CONFIGURATION ========
CLIENT_ID = "7e33ea7c3592494fb69178950b6bb49a"
CLIENT_SECRET = "161159c40cdc484db53ab42413d38652"
redirect_uri="http://127.0.0.1:8888/callback"

# You can get these from the Spotify playlist URLs
SOURCE_PLAYLIST_ID = "https://open.spotify.com/playlist/0WzC9pIbPwBTSLSgedvPHU?si=d35ae84c0b6848b3"  # the one you want to scan
TARGET_PLAYLIST_ID = "https://open.spotify.com/playlist/5jUWUoJtZhRtshPJReKwuq?si=9fe593b2a6384bfd"  # the one to copy Drake tracks into

# ======== SETUP SPOTIFY AUTH ========
scope = "playlist-read-private playlist-modify-public playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=redirect_uri,
    scope=scope
))

# ======== FUNCTION TO FILTER DRAKE TRACKS ========
def get_drake_tracks_from_playlist(sp, playlist_id):
    drake_tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    for item in tracks:
        track = item['track']
        if track and any(artist['name'].lower() == 'drake' for artist in track['artists']):
            drake_tracks.append(track['uri'])

    return drake_tracks

# ======== FUNCTION TO ADD TRACKS TO TARGET PLAYLIST ========
def add_tracks_to_playlist(sp, playlist_id, track_uris):
    for i in range(0, len(track_uris), 100):
        sp.playlist_add_items(playlist_id, track_uris[i:i+100])

# ======== MAIN SCRIPT LOGIC ========
if __name__ == "__main__":
    drake_tracks = get_drake_tracks_from_playlist(sp, SOURCE_PLAYLIST_ID)

    if drake_tracks:
        add_tracks_to_playlist(sp, TARGET_PLAYLIST_ID, drake_tracks)
        print(f"✅ Added {len(drake_tracks)} Drake tracks to your target playlist.")
    else:
        print("❌ No Drake tracks found in the source playlist.")
