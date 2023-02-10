import spotipy
from .authController import create_spotify_oauth


def get_playlists(limit=50, offset=0):
    sp = spotipy.Spotify(oauth_manager=create_spotify_oauth())

    results = {}
    while True:
        query = sp.current_user_playlists(limit=limit, offset=offset)
        for item in query['items']:
            results[item['id']] = {
                'name': item['name'],
                'total': item['tracks']['total'],
                'external_url': item['external_urls']['spotify']
            }

        if query['next'] is not None:
            offset += limit
        else:
            break
    return results

