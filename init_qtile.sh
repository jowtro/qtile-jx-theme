#!/bin/bash

# Init wallpaper
nitrogen --restore &

#Initialize window composite manager
picom &

# email app
thunderbird &

# need to run the script below in order to the NetWatcher to work.
nohup python3.9 $HOME/.config/qtile/test_widget.py &