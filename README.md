# TurnH264
## A simple GUI program that converts the selected video into H264 using FFmpeg.

<img src="screenshot.png">

How to run from source (Every OS): </br>
Install PySide6: `pip install PySide6` </br>
To use the FFmpeg auto-downloader, install wget: `pip install wget` </br>
Otherwise, place an `ffmpeg` executable in the same directory as `TurnH264.py` </br>
FFmpeg builds are available at https://www.ffmpeg.org/download.html </br>
Everything should work on Windows and Linux, while it is not tested on other systems, it should work on any machine that supports Python and FFmpeg. </br>

### Would like to implement:
-   [X] Progress bar
-   [X] FFmpeg downloader
-   [ ] Proper macOS support
-   [ ] FFmpeg NVENC build support