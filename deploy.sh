#!/bin/bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
cd /home/pi/StoryTrolley/server
pwd
pkill node && npm install && node server.js --client ../client/dist &
pwd

DISPLAY=:0 chromium-browser 'http://localhost:8000' --start-fullscreen
