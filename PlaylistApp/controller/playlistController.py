from flask import Blueprint, jsonify, abort
from PlaylistApp import sp

playlist_blueprint = Blueprint('playlist_bp', __name__)


@playlist_blueprint.route('/api/hello', methods=['GET'])
def hello():
    results = sp.current_user_playlists(limit=1)
    print(results)
    playlist_id = None
    for item in results['items']:
        print('Name:', item['name'])
        print('Id:', item['id'])
        playlist_id = item['id']

    playlist = sp.playlist_items(playlist_id)
    print(playlist)
    return jsonify(playlist)
