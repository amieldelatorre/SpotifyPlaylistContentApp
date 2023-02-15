from flask import Blueprint, render_template, send_from_directory, after_this_request, redirect, send_file
from .authController import create_login_url, login_required
from .services import get_playlists, get_playlist_content, get_user_id
import pathlib, os, tarfile, shutil

frontend_blueprint = Blueprint('frontend_bp', __name__)


@frontend_blueprint.route("/")
@login_required
def hello():
    return render_template('home.html',
                           title='Home',
                           playlists=get_playlists())


@frontend_blueprint.route("/login")
def login():
    return render_template('login.html',
                           title="Login",
                           login_link=create_login_url())


@frontend_blueprint.route("/download")
@login_required
def download():
    temp_folder_path = os.path.join(pathlib.Path().resolve(), "temp")
    user_id = get_user_id()
    temp_user_folder_path = os.path.join(temp_folder_path, user_id)

    if os.path.exists(temp_user_folder_path):
        shutil.rmtree(temp_user_folder_path)
    os.mkdir(temp_user_folder_path)

    playlists = get_playlists()
    for key in playlists.keys():
        playlists[key]["content"] = get_playlist_content(key)

        restricted_chars = ['/', '\\', '<', '>', '"', ':', '|', '?', '*']
        restricted_chars_in_playlist_name = [ char for char in restricted_chars if char in playlists[key]['name'] ]
        if restricted_chars_in_playlist_name:
            playlist_file_path = os.path.join(temp_user_folder_path, f"{key}.csv")
        else:
            playlist_file_path = os.path.join(temp_user_folder_path, playlists[key]['name'] + ".csv")
            if os.path.exists(playlist_file_path):
                playlist_file_path = os.path.join(temp_user_folder_path, f"{key}.csv")

        write_playlist_to_file(playlist_file_path, playlists[key], key)

    archived_file_name = f"{temp_user_folder_path}.tar.gz"

    with tarfile.open(archived_file_name, "w:gz") as tar:
        tar.add(temp_user_folder_path, arcname=os.path.basename(temp_folder_path))

    @after_this_request
    def clean_up(response):
        shutil.rmtree(temp_user_folder_path)

        # This causes an error in windows but works fine in Linux based systems
        # Because Linux lets the file be read even after deletion if there is still an open file pointer to it
        # https://stackoverflow.com/questions/24612366/delete-an-uploaded-file-after-downloading-it-from-flask
        os.remove(archived_file_name)
        return response

    return send_file(archived_file_name)


@frontend_blueprint.route("/delete")
def delete():
    temp_folder_path = os.path.join(pathlib.Path().resolve(), "temp")
    user_id = get_user_id()
    temp_user_folder_path = os.path.join(temp_folder_path, user_id)
    archived_file_name = f"{temp_user_folder_path}.tar.gz"
    os.remove(archived_file_name)
    return redirect("/")


def write_playlist_to_file(playlist_file_path, playlist, playlist_id):
    with open(playlist_file_path, "w", encoding="utf-32") as file:
        file.write(f"Playlist Name,{playlist['name']}\n")
        file.write(f"Playlist Id,{playlist_id}\n")
        file.write(f"Total number of tracks,{playlist['total']}\n")
        for content in playlist['content']:
            artists = ""

            if content is None or content['track'] is None:
                continue
            elif content['track']['artists'] is None:
                artists = "None"
            else:
                for i in range(len(content['track']['artists'])):
                    artists += content['track']['artists'][i]['name']
                    if i != len(content['track']['artists']) - 1:
                        artists += "|"

            if 'spotify' not in content['track']['external_urls']:
                file.write(f"{content['track']['name']},{artists},None\n")
            else:
                file.write(f"{content['track']['name']},{artists},{content['track']['external_urls']['spotify']}\n")
