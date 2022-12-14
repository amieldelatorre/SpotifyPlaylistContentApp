import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import requests


def get_playlist_names(query_result, playlists_dict):
    for item in query_result['items']:
        print('Name:', item['name'], end=" ")
        print('Id:', item['id'])
        playlists_dict[item['name']] = item['id']


load_dotenv()

scope = "user-library-read playlist-read-collaborative playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def get_all_playlists():
    limit = 10
    offset = 0
    all_playlists = dict()
    results = sp.current_user_playlists(limit=limit, offset=offset)
    print(results)

    next_query = results['next']
    get_playlist_names(results, all_playlists)

    while next_query is not None:
        offset += limit
        results = sp.current_user_playlists(limit=limit, offset=offset)
        get_playlist_names(results, all_playlists)
        next_query = results['next']

    f = open("Out/Playlists.txt", "w", encoding="utf-8")
    f.writelines("Playlist Name,Playlist ID\n")
    for key in all_playlists.keys():
        f.writelines("{},{}\n".format(key, all_playlists[key]))
    f.close()


def get_items_in_playlists(filename):
    file = open(filename, "r", encoding="utf-8")
    first_line = file.readline()
    raw_list = file.readlines()
    file.close()

    osErrorCatchName = 1

    for playlist in raw_list:
        try:
            p_line = playlist.split(",")
            playlist_name = p_line[0]
            playlist_id = p_line[1].strip()
            description = sp.playlist(playlist_id)['description']

            try:
                playlist_file = open("Out/Playlists/{}.txt".format(playlist_name), "w", encoding="utf-8")
            except OSError:
                playlist_file = open("Out/Playlists/{}.txt".format(osErrorCatchName), "w", encoding="utf-8")
                osErrorCatchName += 1

            playlist_file.writelines("{}\n".format(playlist_name))
            playlist_file.writelines("Description: {}\n\n".format(description))
            playlist_file.writelines("Song Name,Artists(s),Date Added,Added By\n")

            limit = 100
            offset = 0
            next_query = True

            while next_query is not None:
                playlist_items = sp.playlist_items(playlist_id, limit=limit, offset=offset)
                for item in playlist_items['items']:
                    track = item['track']
                    if track is None:
                        continue
                    date_added = item['added_at']
                    added_by = item['added_by']['id']

                    song_name = item['track']['name']
                    artist_list = []
                    for artist in item['track']['artists']:
                        artist_list.append(artist['name'])

                    playlist_file.writelines("{},{},{},{}\n".format(song_name, "+".join(artist_list), date_added, added_by))

                next_query = playlist_items['next']
                if next_query is not None:
                    offset += limit

            playlist_file.close()
            print(playlist_name, "done!")
        except requests.exceptions.HTTPError:
            pass

        except spotipy.exceptions.SpotifyException:
            pass



filename = "Out/Playlists.txt"
get_items_in_playlists(filename)


playlist_id = '2xp36G5xeA9nZB4vhgZayh'
playlist = sp.playlist_items(playlist_id)
#print(playlist)
