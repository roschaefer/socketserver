# trolley-server

# fire up HTTP Server
in ~/StoryTrolley/client/dist 
python3 -m http.server &

# launch WebSockets
in ~/StoryTrolley/server
python3 ws.py &

# run browser
DISPLAY=:0 chromium-browser 'http://localhost:8000/' --start-fullscreen
