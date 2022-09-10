# coding: utf-8
import os
import shutil
import sys
import tarfile
import zipfile

import wget


def download():

    dl = False
    print("Downloading FFmpeg, please wait...")

    #FFmpeg latest build links, thanks BtbN!
    if sys.platform == "win32":
        wget.download('https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip')
    elif sys.platform == "linux":
        wget.download('https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz')
    print("\nExtracting FFmpeg, please wait...")
    if sys.platform == "win32":
        with zipfile.ZipFile('./ffmpeg-master-latest-win64-gpl.zip', 'r') as zip_ref: 
            zip_ref.extract('ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe')
            zip_ref.extract('ffmpeg-master-latest-win64-gpl/bin/ffprobe.exe')
            shutil.move('ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe', 'ffmpeg.exe')
            shutil.move('ffmpeg-master-latest-win64-gpl/bin/ffprobe.exe', 'ffprobe.exe')
            shutil.rmtree('./ffmpeg-master-latest-win64-gpl')
        os.remove('ffmpeg-master-latest-win64-gpl.zip')
    elif sys.platform == "linux":
        with tarfile.open('./ffmpeg-master-latest-linux64-gpl.tar.xz', 'r') as tar_ref:
            tar_ref.extract('ffmpeg-master-latest-linux64-gpl/bin/ffmpeg')
            tar_ref.extract('ffmpeg-master-latest-linux64-gpl/bin/ffprobe')
            shutil.move('ffmpeg-master-latest-linux64-gpl/bin/ffmpeg', 'ffmpeg')
            shutil.move('ffmpeg-master-latest-linux64-gpl/bin/ffprobe', 'ffprobe')
            shutil.rmtree('./ffmpeg-master-latest-linux64-gpl')
        os.remove('ffmpeg-master-latest-linux64-gpl.tar.xz')
    print("Done, starting program!")
