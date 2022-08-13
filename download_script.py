# coding: utf-8
import os
import sys
import wget
import shutil
import tarfile
import zipfile

def download():

    ffmpeg_win_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    ffmpeg_linux_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz"

    dl = False
    print("Downloading FFmpeg, please wait...")
    if sys.platform == "win32":
        wget.download(ffmpeg_win_url)
        dl = True
    elif sys.platform == "linux":
        wget.download(ffmpeg_linux_url)
        dl = True
    if dl == True:
        print("\nExtracting FFmpeg, please wait...")
        if sys.platform == "win32":
            with zipfile.ZipFile('./ffmpeg-master-latest-win64-gpl.zip', 'r') as zip_ref: 
                zip_ref.extract('ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe')
                shutil.move('ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe', 'ffmpeg.exe')
                shutil.rmtree('./ffmpeg-master-latest-win64-gpl')
            os.remove('ffmpeg-master-latest-win64-gpl.zip')
        elif sys.platform == "linux":
            with tarfile.open('./ffmpeg-master-latest-linux64-gpl.tar.xz', 'r') as tar_ref:
                tar_ref.extract('ffmpeg-master-latest-linux64-gpl/bin/ffmpeg')
                shutil.move('ffmpeg-master-latest-linux64-gpl/bin/ffmpeg', 'ffmpeg')
                shutil.rmtree('./ffmpeg-master-latest-linux64-gpl')   
            os.remove('ffmpeg-master-latest-linux64-gpl.tar.xz')
    print("Done, starting program!")