# LikeThisSong-SpotifyAPI

## What it does?
### It adds (if there is a song playing) the current song to a playlist, with just a press in the "home" key, using the Spotify API.  
### If you press the "end" key it stops listen to key events.
### Creates a log file.
  
## What I've learned?
### OAuth 2.0 authentication
### Observer Pattern
### Manipulate datetime format  

## Dependencies
- keyboard module
- secrets module

## Requirements
### 1 - Get the authorization code:
- Create an app into spotify api  
- Add redirect_uri: http://localhost:8888/callback  
- Insert client_id in the link below  
- https://accounts.spotify.com/authorize?client_id=<client_id>&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8888%2Fcallback%2F&scope=user-read-playback-state%20playlist-modify-private  
- Past it in the browser  
- Accept terms  
- Get the auth code after "code=" in the url  
  
### 2- Request auth token:
- Add the client_id, client_secret, auth_code that you got before in the following script:  
  
encoded = base64.b64encode(bytes(f"{<client_id>}:{<client_secret>}", "utf-8")).decode("ascii")  
code = '<auth_code>'  
token_endpoint = 'https://accounts.spotify.com/api/token'  
headers = {'Authorization': 'Basic ' + encoded, 'Content-Type': 'application/x-www-form-urlencoded'}
payload = {'grant_type': 'authorization_code',
               'code': code,
               'redirect_uri': http://localhost:8888/callback  
response = requests.post(token_url, data=payload, headers=headers)  
token = dict(response.json())['access_token']  
refresh_token = dict(response.json())['refresh_token']  
print(token)  
print(refresh_token)  
  
 - your token and refresh_token will be prompted in your console
   
 ### 3- Edit secrets.py file:
 - Add your client_id and client_secret  
 - Add your token  
 - Add your refresh_token  
   
 ### 4- Change the playlist id in the line 88, after /playlists/  
 To get your playlist id: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-list-users-playlists  
