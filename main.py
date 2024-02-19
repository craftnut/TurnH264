# coding: utf-8
import argparse
import os
import signal
import subprocess
import sys
import threading
import time
from ctypes import alignment
from get_ffmpeg import check_ffmpeg

from PySide6 import QtCore, QtGui, QtWidgets

platform = sys.platform()

args = argparse.ArgumentParser()
args.add_argument(
    '--ignore__ffmpeg', required = False, default = False, action = "store_true",
    help = "Ignores FFmpeg if installed system-wide and available in PATH"
)
args.add_argument(
    '--force_unsupported_platform', required = False, default = False, action = "store_true",
    help = "Force unsupported platform condition, for debugging purposes only!!"
)


args = args.parse_args()

ffmpeg_path = check_ffmpeg(args.ignore_ffmpeg, platform)

if ffmpeg_path == "unsupported" | args.force_unsupported_platform :
    