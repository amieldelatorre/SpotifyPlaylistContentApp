FROM python:3.11.2-buster
WORKDIR /spotilist

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 8080
# Running the host as "127.0.0.1" does not work
CMD [ "waitress-serve", "--host" , "0.0.0.0", "--call", "PlaylistApp:create_app"]