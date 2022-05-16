import json
import keyboard
import requests
import base64
import secrets
from datetime import datetime, timedelta


def info_datetime(expiration=False):
    time = datetime.now()  # current time
    if expiration:  # calculate expiration flag
        time = datetime.now() + timedelta(minutes=50)
    return time.strftime("%d/%m/%Y %H:%M:%S")


# controll and set auth parameters, update the Manager's token
class AuthController:
    def __init__(self):
        self.observers = []  # list of structures who listen to AuthController
        self.current_token = secrets.token
        self.current_timeflag = secrets.expires_in
        self.refresh_token = secrets.refresh_token

    def register_observer(self, observer):
        self.observers.append(observer)
        self.notify_observers()  # updates the newly added Manager's token

    def notify_observers(self):
        size = len(self.observers)
        for observer in range(0, size):  # for each observer in the observers list
            obs = self.observers[observer]
            obs.update(self.current_token)  # update observer's token

    def calculateFlag(self):
        flag = info_datetime(expiration=True)
        self.current_timeflag = flag  # new flag = now + 50 minutes by info_datetime function

    def updateSecrets(self):
        # save client id and secret to rewrite safely.
        client_id = secrets.client_id
        client_secret = secrets.client_secret

        # updates secrets with current parameters
        secrets_file = open('secrets.py', 'w')
        secrets_file.write(f'token = "{self.current_token}"\n')
        secrets_file.write(f'refresh_token = "{self.refresh_token}"\n')
        secrets_file.write(f'client_id = "{client_id}"\n')
        secrets_file.write(f'client_secret = "{client_secret}"\n')
        secrets_file.write(f'expires_in = "{self.current_timeflag}"\n')

    def getNewToken(self):
        # refreshes token's access
        client_id = secrets.client_id
        client_secret = secrets.client_secret
        encoded = base64.b64encode(bytes(f"{client_id}:{client_secret}", "utf-8")).decode("ascii")  # encode de client_id:client_secret to pass on headers
        token_url = 'https://accounts.spotify.com/api/token'  # endpoint to take a [new] token

        headers = {'Authorization': 'Basic ' + encoded, 'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'grant_type': 'refresh_token',
                   'refresh_token': self.refresh_token}

        req = requests.post(token_url, data=payload, headers=headers)

        try:
            self.current_token = dict(req.json())['access_token']  # get access token = str from response of the request and pass it to current_token secrets' parameter
        except Exception as e:
            file.write(f'{info_datetime()} - {str(e)}')
        else:
            self.updateSecrets()

    def refreshToken(self):
        # oganize flow of a refresh token update
        self.calculateFlag()
        self.getNewToken()
        self.notify_observers()

    def verifyExpiration(self):
        current_time = info_datetime()
        if current_time >= self.current_timeflag:  # if NOW is later then the expiration timeflag
            file.write('Token refreshed!\n')
            self.refreshToken()  # refresh expiration timeflag


# responsible for adding the song to the playlist
class Manager:
    def __init__(self):
        self.song_uri = 'https://api.spotify.com/v1/me/player'  # endpoint to get song_uri
        self.add_playlist_url = 'https://api.spotify.com/v1/playlists/2SEE0wXvr18raCb3HyZIQn/tracks'  # endpoint to add song to playlist
        self.token = ''

    def update(self, token):
        self.token = token

    def addToPlaylist(self):
        headers = {'Authorization': 'Bearer ' + self.token, 'Content-Type': 'application/json'}
        player_items_req = requests.get(url=self.song_uri, headers=headers)

        try:
            # get song uri, song name and artist name
            song_uri = [dict(player_items_req.json())['item']['uri']]
            song_name = dict(player_items_req.json())['item']['name']
            artist_name = dict(player_items_req.json())['item']['artists'][0]['name']
        except:
            file.write(f'{info_datetime()} - There is no song playing right now.\n')  # if fail then player is off
        else:
            # add song to playlist
            payload = {"uris": song_uri}
            requests.post(url=self.add_playlist_url, headers=headers, data=json.dumps(payload))
            file.write(f'{info_datetime()} - Added {song_name} - {artist_name}\n')


# begin
authenticanting = 'Authenticating'
file = open('AutoAddSpotify.log', 'w')
file.write(f'\n{info_datetime()}  - Starting program...\n\n')
file.write(f'{"-" * len(authenticanting)}\n{authenticanting}\n{"-" * len(authenticanting)}\n')

# start manager and auth_controller, adding manager to the auth_controller's observers list
manager = Manager()
auth_controller = AuthController()
auth_controller.register_observer(manager)

file.write(f'\n{info_datetime()} - Connected!\n')
file.write(f'token_expires_in = {auth_controller.current_timeflag}\n')

# listen to events
file.write(f'\n{info_datetime()} - Waiting for events...\n')

while True:
    auth_controller.verifyExpiration()
    if keyboard.read_key() == "home":  # add song to playlist
        manager.addToPlaylist()
    elif keyboard.read_key() == "end":  # exit
        file.write(f'\n\n{info_datetime()} - Leaving\n')
        file.close()
        break
