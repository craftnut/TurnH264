import subprocess

avail = "FFmpeg already installed, starting program!"
ff_linux = "ffmpeg-master-latest-linux64-gpl"
ff_windows = "ffmpeg-master-latest-win64-gpl"

def check_ffmpeg(skip, platform):
    try:
        if not skip:
            subprocess.Popen(['ffmpeg'])
            print(avail)
            return "ffmpeg"
        else:
            raise Exception()
    except: 
        get_ffmpeg(platform)
        
def get_ffmpeg(platform):
    import wget
    
    try:
        subprocess.Popen("./ffmpeg")
        print(avail)
        return "./ffmpeg"
    except:
        if platform == "win32":
            wget.download('https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip')
            extract(platform)
        elif platform == "linux":
            wget.download('https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz')
            extract(platform)
        else:
            return "unsupported"
    
def extract(platform):
    import shutil
    import os
    
    if platform != "win32":
        import tarfile
        
        with tarfile.open(f"./{ff_linux}.tar.xz", 'r') as ff_archive:
            ff_archive.extract(f"{ff_linux}/bin/ffmpeg")
            shutil.move(f"{ff_linux}/bin/ffmpeg", 'ffmpeg')
            shutil.rmtree(f"./{ff_linux}")
            os.remove(f"{ff_linux}.tar.xz")
            return "./ffmpeg"
    else:
        import zipfile
        
        with zipfile.ZipFile(f"./{ff_windows}.zip", "r") as ff_archive:
            ff_archive.extract(f"{ff_windows}/bin/ffmpeg")
            shutil.move(f"{ff_windows}/bin/ffmpeg", "ffmpeg")
            shutil.rmtree(f"./{ff_windows}")
            os.remove(f"{ff_windows}.zip")
            return "./ffmpeg.exe"