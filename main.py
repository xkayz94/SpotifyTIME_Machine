import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
url = 'https://example.com/?code=AQBdAAB6D-YK9ffQTy7rmZiENsp0Su9T9CipB5zZx8FDcoHIdpScmIA_fynATzLIbrvZJVVjuM_ei81QM2TKmdFIM7KOLYlBp4BCEiz-g4fy99bG7t4rjqEk4NlXAHX-aGk2_lrsRfATu0niAjxv2IShODvaHw'
Client_ID = '0792d63c9d3844378f35a47fbd9903cb'
Client_Secret = 'c84175b00a64458e90c08f8f372801e9'
REDIRECT_URIS = 'http://example.com'

PLAYLIST_NAME = 'my_playlist'


soap = BeautifulSoup()
travel_date = input('Which year do you want to travel to? '
                    'Type the date in this format: YYYY-MM-DD:')


endpoint = f'https://www.billboard.com/charts/hot-100/{travel_date}/'

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

response = requests.get(url=endpoint, headers=header)
billboard_web_page = response.text
soup = BeautifulSoup(billboard_web_page, 'html.parser')

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]




sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=Client_ID,
        scope = "playlist-modify-private",
        client_secret=Client_Secret,
        redirect_uri=REDIRECT_URIS,
        cache_path="token.txt"))

user_id = sp.current_user()["id"]
print(user_id)


# playlist = sp.user_playlist_create(user=user_id,
#                                    name=PLAYLIST_NAME,
#                                    public=False,
#                                    collaborative=False,
#                                    description='For gym')
#
# playlist_id = playlist['id']
#

song_uris = []
year = travel_date.split('-')[0]

for song in song_names:
    result = sp.search(q=f'track:{song} year:{year}', type='track')
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")



playlist_name = "My Python Playlist(Songs Names Only)"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)

if song_uris:
    sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)
    print(f"Playlist'{playlist_name}'has been created successfully!")
else:
    print("No valid tracks found. Playlist not created")