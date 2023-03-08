# SpotiList
List the details of your playlists and other user data.

## How to Run
1. Setup a `.env` file.

**Required variables in the .env file**
```shell
SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET
SPOTIPY_REDIRECT_URI
SPOTIPY_SCOPE
FLASK_APP
FLASK_ENV
SECRET_KEY
```
2. Install the requirements and run the program
```shell
$ python -m venv venv
$ source .\venv\Scripts\activate ./venv/scripts/activate 
$ pip install -r ./requirements.txt
$ flask --app app run
$ # deactivate # To deactivate the virtualenv
```
