# To H264
## A simple GUI program that converts the selected video into H264 using FFmpeg.
###### When in doubt, turn to H264.

How to run the executable (Windows):
Download the package from releases
Place `ffmpeg.exe` alongside `TurnH264.exe`
FFmpeg builds are available at https://www.ffmpeg.org/download.html

How to run from source (Linux, macOS):
Install PySide6
`pip install PySide6`
Place an `ffmpeg` executable in the same directory as `TurnH264.py`
(Linux: make sure FFmpeg is marked executable!)
FFmpeg builds are available at https://www.ffmpeg.org/download.html
Everything should work as intended.
(Please do note that this program is untested for macOS as neither me nor any of my friends have Apple hardware)

Currently implemented:
1. Video bitrate choice
2. Audio bitrate choice
3. Graphical file browsing
4. Amount of threads to use

Would like to implement:
1. Progress bar
2. NVENC and VCE

Xpsycho's fork was developed alongside this master branch during pre-release hence the differences in variable names and major differences in code layout.