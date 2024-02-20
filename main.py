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
from windows.unsupported_dialog import unsupported_dialog
from windows.advanced_options_dialog import advanced_options

from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QComboBox,
    QWidget,
)

# Global Vars
threads = os.cpu_count()

quality = 22

encoder_preset = "medium"
if not threads < 6:
    encoder_threads = 4
else:
    encoder_threads = 2
    
audio_codec = "AAC"
audio_bitrate = 128

args = argparse.ArgumentParser()
args.add_argument(
    '--ignore_ffmpeg', required = False, default = False, action = "store_true",
    help = "Ignores FFmpeg if installed system-wide and available in PATH"
)
args.add_argument(
    '--force_unsupported_platform', required = False, default = False, action = "store_true",
    help = "Force unsupported platform condition, for debugging purposes only!!"
)
args = args.parse_args()

if args.force_unsupported_platform == True:
    platform = "FakeOS"
else:
    platform = sys.platform

ffmpeg_path = check_ffmpeg(args.ignore_ffmpeg, platform)
print(ffmpeg_path)

if ffmpeg_path == "unsupported":
    unsupported_dialog(platform)

def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.resize(300, 155)
    mw.show()
    sys.exit(app.exec())

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)
        self.setWindowTitle("TurnH264")
        
        in_label = QLabel(
            "Choose input video:",
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        in_file = QLineEdit(
        )
        choose_in_file = QPushButton(
            "Pick File"
        )
        
        out_label = QLabel(
            "Choose output location:",
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        out_file = QLineEdit(
        )
        choose_out_location = QPushButton(
            "Choose" 
        )
        
        open_advanced_options = QPushButton(
            "Advanced Options"
        )
        open_advanced_options.clicked.connect(get_advanced_settings)
        go = QPushButton(
            "Go"
        )
        
        layout.addWidget(in_label, 0, 0, 1, 3)
        layout.addWidget(in_file, 1, 0, 1, 2)
        layout.addWidget(choose_in_file, 1, 2, 1, 1)
        
        layout.addWidget(out_label, 2, 0, 1, 3)
        layout.addWidget(out_file, 3, 0, 1, 2)
        layout.addWidget(choose_out_location, 3, 2, 1, 1)
        
        layout.addWidget(open_advanced_options, 4, 0, 1, 2)
        layout.addWidget(go, 4, 2, 1, 1)       

def get_advanced_settings(): 
    (
        quality,
        encoder_preset,
        encoder_threads,
        audio_codec,
        audio_bitrate
    ) = advanced_options(threads)
    print(quality, encoder_preset, encoder_threads, audio_codec, audio_bitrate) # Remove when feature fully implemented

main()