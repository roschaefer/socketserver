# trolley-server

## fire up HTTP Server
in `~/StoryTrolley/client/dist`
``` bash
python3 -m http.server &
```

## launch WebSockets
in `~/StoryTrolley/server`
```bash
python3 ws.py &
```

## run browser
```bash
DISPLAY=:0 chromium-browser 'http://localhost:8000/' --start-fullscreen
```
