import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = "REPLACE"
client_secret = "REPLACE"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="Day 46 Musical Time Machine/token.txt"
    )
)
user_id = sp.current_user()["id"]

artist_name = "Joji"
#Searching Spotify for songs by the artist
song_uris = []

result = sp.search(q=f"artist:{artist_name}", type="track")

while result["tracks"]["items"]:
    for item in result["tracks"]["items"]:
        # Using this method will only add songs that have the same name exactly
        if item["album"]["artists"][0]["name"] == artist_name:
            song_uris.append(item["uri"])
        # Using this method will add any song with the match name
        # if artist_name in item["album"]["artists"][0]["name"]:
        #     song_uris.append(item["uri"])
        
    if result["tracks"]["next"]:
        result = sp.next(result["tracks"])
    else:
        break

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{artist_name} playlist", public=False)

#Adding songs found into the new playlist
for i in range(0, len(song_uris), 100):
    batch = song_uris[i:i+100]
    sp.playlist_add_items(playlist_id=playlist["id"], items=batch)
print("Enjoy")