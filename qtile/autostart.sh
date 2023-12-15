#!/bin/sh

xrandr --output Virtual-1 --mode 1920x1080 
xrandr --output Virtual-2 --mode 1920x1080 --right-of Virtual-1 


feh --bg-fill --randomize ~/Documents/Wallpapers/*

picom -b &
