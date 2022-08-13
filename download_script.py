# coding: utf-8
import os
import sys
import shutil
import tarfile
import zipfile
import requests

def download():

    ffmpeg_win_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    ffmpeg_linux_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz"

    dl = False
    if sys.platform == "win32":
        open("ffmpeg.zip", "wb").write(requests.get(ffmpeg_win_url).content)
        dl = True
    elif sys.platform == "linux":
        open("ffmpeg.tar.xz", "wb").write(requests.get(ffmpeg_linux_url).content)
        dl = True
    if dl == True:
        if sys.platform == "win32":
            with zipfile.ZipFile('./ffmpeg.zip', 'r') as zip_ref: 
                zip_ref.extract('ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe')
                shutil.move('ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe', 'ffmpeg.exe')
                shutil.rmtree('./ffmpeg-master-latest-win64-gpl')
            os.remove('ffmpeg.zip')
        elif sys.platform == "linux":
            with tarfile.open('./ffmpeg.tar.xz', 'r') as tar_ref:
                tar_ref.extract('ffmpeg-master-latest-linux64-gpl/bin/ffmpeg')
                shutil.move('ffmpeg-master-latest-linux64-gpl/bin/ffmpeg', 'ffmpeg')
                shutil.rmtree('./ffmpeg-master-latest-linux64-gpl')   
            os.remove('ffmpeg.tar.xz')