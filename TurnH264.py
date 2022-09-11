# coding: utf-8
import os
import signal
import subprocess
import sys
import threading
import time
from ctypes import alignment

from PySide6 import QtCore, QtGui, QtWidgets

import download_script

try: #to see if FFmpeg is available system-wide
    subprocess.Popen(['ffmpeg', '-version'],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ffmpeg_path = "ffmpeg"
    ffprobe_path = "ffprobe"
    print("FFmpeg already installed, starting program!")
except: #if it's not, check if it's already been downloaded
    if sys.platform == "win32" and os.path.exists('./ffmpeg.exe'):
        ffmpeg_path = "./ffmpeg.exe"
        ffprobe_path = "./ffprobe.exe"
        print("FFmpeg already installed, starting program!")
    elif sys.platform == "linux" and os.path.exists('./ffmpeg'):
        ffmpeg_path = "./ffmpeg"
        ffprobe_path = "./ffprobe"
        print("FFmpeg already installed, starting program!")
    elif sys.platform == "win32" or sys.platform == "linux": #if not, download it
        download_script.download()
        if sys.platform == "win32":
            ffmpeg_path = "./ffmpeg.exe"
            ffprobe_path = "./ffprobe.exe"
        elif sys.platform == "linux":
            ffmpeg_path = "./ffmpeg"
            ffprobe_path = "./ffprobe"
    elif sys.platform == "darwin" and os.path.exists('./ffmpeg.app'):
        ffmpeg_path = "./ffmpeg.app"
        ffprobe_path = "./ffprobe.app"
    else:
        print("FFmpeg auto-downloader either failed or is not compatible on this device, please download FFmpeg manually following the README.")
        exit(1)

class MainWindow(QtWidgets.QWidget): #Main class
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TurnH264")

        #Import fonts
        QtGui.QFontDatabase.addApplicationFont("fonts/IBMPlexSans-Regular.ttf")
        QtGui.QFontDatabase.addApplicationFont("fonts/IBMPlexSans-Semibold.ttf")

        self.go_button = QtWidgets.QPushButton("Go")
        self.cancel_button = QtWidgets.QPushButton("Cancel Process")
        self.choose_file_button = QtWidgets.QPushButton("Choose a File")
        self.choose_output_button = QtWidgets.QPushButton("Choose output")
        self.overwrite_existing_button = QtWidgets.QPushButton("Overwrite")
        self.dont_overwrite_button = QtWidgets.QPushButton("Cancel")
        self.about_button = QtWidgets.QPushButton("Program Information")
        self.help_button = QtWidgets.QPushButton("Program Help")
        self.threads = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.threads.setTickInterval(1)
        self.threads.setMaximum(os.cpu_count())
        self.threads.setValue(os.cpu_count()/2)
        self.audio_bitrate = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.audio_bitrate.setMinimum(64/32)
        self.audio_bitrate.setMaximum(256/32)
        self.audio_bitrate.setValue(160/32)
        self.video_quality = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.video_quality.setMinimum(0)
        self.video_quality.setMaximum(51)
        self.video_quality.setValue(22)
        self.input_dialog = QtWidgets.QLabel("Choose input video:",
                                             alignment=QtCore.Qt.AlignCenter)
        self.thread_dialog = QtWidgets.QLabel(f"Select the number of CPU threads to use: {self.threads.value()} / {os.cpu_count()}",
                                              alignment=QtCore.Qt.AlignCenter)
        self.audio_bitrate_dialog = QtWidgets.QLabel(f"Select the audio bitrate: {self.audio_bitrate.value()*32}",
                                                     alignment=QtCore.Qt.AlignCenter)
        self.input_file = QtWidgets.QLineEdit(self,
                                              alignment=QtCore.Qt.AlignCenter)
        self.output_dialog = QtWidgets.QLabel("Choose where to save output:",
                                              alignment=QtCore.Qt.AlignCenter)
        self.output_file = QtWidgets.QLineEdit(self,
                                               alignment=QtCore.Qt.AlignCenter)
        self.audio_codec_text = QtWidgets.QLabel("Use AAC or Opus?",
                                                 alignment=QtCore.Qt.AlignCenter)
        self.encoder_preset_text = QtWidgets.QLabel("Select Encoder Preset:",
                                                    alignment=QtCore.Qt.AlignCenter)
        self.progress_bar_text = QtWidgets.QLabel("",
                                                  alignment=QtCore.Qt.AlignCenter)
        self.video_quality_text = QtWidgets.QLabel(f"H264 quality setting: {self.video_quality.value()}",
                                                   alignment=QtCore.Qt.AlignCenter)
        self.resolution_text = QtWidgets.QLabel("Change resolution (leave blank for original):",
                                                alignment=QtCore.Qt.AlignCenter)
        self.resolution = QtWidgets.QLineEdit(self,
                                              alignment=QtCore.Qt.AlignCenter)
        self.audio_codec = QtWidgets.QComboBox(self)
        self.audio_codec.addItems(["AAC", "Opus"])
        self.encoder_preset = QtWidgets.QComboBox(self)
        self.encoder_preset.addItems(["veryfast", "faster", "fast", "medium", "slow", "slower"])
        self.encoder_preset.setCurrentIndex(3)

        # column, row, height, width
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.input_dialog, 0, 0, 1, 1)
        self.layout.addWidget(self.input_file, 1, 1, 1, 1)
        self.layout.addWidget(self.choose_file_button, 1, 0, 1, 1)
        self.layout.addWidget(self.output_dialog, 2, 0, 1, 1)
        self.layout.addWidget(self.output_file, 3, 1, 1, 1)
        self.layout.addWidget(self.choose_output_button, 3, 0, 1, 1)
        self.layout.addWidget(self.resolution_text, 4, 0, 1, 1)
        self.layout.addWidget(self.resolution, 4, 1, 1, 1)
        self.layout.addWidget(self.video_quality_text, 5, 0, 1, 1)
        self.layout.addWidget(self.video_quality, 5, 1, 1, 1)
        self.layout.addWidget(self.encoder_preset_text, 6, 0, 1, 1)
        self.layout.addWidget(self.encoder_preset, 6, 1, 1, 1)
        self.layout.addWidget(self.audio_codec_text, 7, 0, 1, 1)
        self.layout.addWidget(self.audio_codec, 7, 1, 1, 1)
        self.layout.addWidget(self.audio_bitrate_dialog, 8, 0, 1, 1)
        self.layout.addWidget(self.audio_bitrate, 8, 1, 1, 1)
        self.layout.addWidget(self.thread_dialog, 9, 0, 1, 1)
        self.layout.addWidget(self.threads, 9, 1, 1, 1)
        self.layout.addWidget(self.go_button, 10, 0, 1, 2)
        self.layout.addWidget(self.cancel_button, 10, 0, 1, 1)
        self.layout.addWidget(self.progress_bar_text, 10, 1, 1, 1)
        self.layout.addWidget(self.overwrite_existing_button, 10, 0, 1, 1)
        self.layout.addWidget(self.dont_overwrite_button, 10, 1, 1, 1)
        self.layout.addWidget(self.about_button, 11, 0, 1, 1,)
        self.layout.addWidget(self.help_button, 11, 1, 1, 1)
        self.overwrite_existing_button.hide()
        self.dont_overwrite_button.hide()
        self.cancel_button.hide()
        self.progress_bar_text.hide()
        
        self.choose_file_button.clicked.connect(self.choose_file)
        self.go_button.clicked.connect(self.go_button_clicked)
        self.threads.valueChanged.connect(self.slider_updated)
        self.audio_bitrate.valueChanged.connect(self.slider_updated)
        self.video_quality.valueChanged.connect(self.slider_updated)
        self.overwrite_existing_button.clicked.connect(self.overwrite_files)
        self.dont_overwrite_button.clicked.connect(self.dont_overwrite_files)
        self.choose_output_button.clicked.connect(self.choose_where_output)
        self.about_button.clicked.connect(self.about_clicked)
        self.help_button.clicked.connect(self.help_clicked)

    class AboutProgram(QtWidgets.QDialog): #Information about the program
        def __init__(self):
            super().__init__()

            self.setWindowTitle("About Program")
            self.about_dialog = QtWidgets.QLabel("TurnH264 is licensed under the Helium License",
                                                alignment=QtCore.Qt.AlignCenter)
            self.about_copyright = QtWidgets.QLabel("TurnH264 is © 2022 craftnut",
                                                alignment=QtCore.Qt.AlignCenter)
            self.about_ffmpeg = QtWidgets.QLabel("FFmpeg is licensed under the GNU GPL license",
                                                alignment=QtCore.Qt.AlignCenter)
            self.with_love = QtWidgets.QLabel("Made with <3 by craftnut",
                                                alignment=QtCore.Qt.AlignCenter)
            self.github_repository = QtWidgets.QLabel('''<a href='https://github.com/craftnut/TurnH264'>View the source code on GitHub</a>''',
                                                alignment=QtCore.Qt.AlignCenter)
            self.github_repository.setOpenExternalLinks(True)

            self.layout = QtWidgets.QVBoxLayout(self)
            self.layout.addWidget(self.about_dialog)
            self.layout.addWidget(self.about_copyright)
            self.layout.addWidget(self.about_ffmpeg)
            self.layout.addWidget(self.with_love)
            self.layout.addWidget(self.github_repository)

    class HelpWindow(QtWidgets.QDialog): #Help window
        def __init__(self):
            super().__init__()

            self.setWindowTitle("Help")
            self.help_output = QtWidgets.QLabel("If you didn't select an output, check the directory for output.mp4",
                                                alignment=QtCore.Qt.AlignCenter)
            self.help_bitrate = QtWidgets.QLabel("Lower values for quality are higher quality, don't ask me why, I wish I knew.",
                                                alignment=QtCore.Qt.AlignCenter)
            self.found_bug = QtWidgets.QLabel("Found a bug? Report it on the GitHub page.",
                                                alignment=QtCore.Qt.AlignCenter)

            self.layout = QtWidgets.QVBoxLayout(self)
            self.layout.addWidget(self.help_output)
            self.layout.addWidget(self.help_bitrate)
            self.layout.addWidget(self.found_bug)

    class FinishDialog(QtWidgets.QDialog): #Dialog when your process finishes
        def __init__(self):
            super().__init__()

            self.setWindowTitle("Finished")
            self.finish_dialog = QtWidgets.QLabel("Your file is done processing, check for output file.")
            self.acknowledged_finish = QtWidgets.QPushButton("Ok")
            self.layout = QtWidgets.QVBoxLayout(self)
            self.layout.addWidget(self.finish_dialog)

    class NoFileDialog(QtWidgets.QDialog): #Warn the user about a lack of input file
        def __init__(self):
            super().__init__()

            self.setWindowTitle("Error")
            self.no_file_dialog = QtWidgets.QLabel("Please select a file.")
            self.acknowledge_lack_of_file = QtWidgets.QPushButton("Ok")
            self.layout = QtWidgets.QVBoxLayout(self)
            self.layout.addWidget(self.no_file_dialog)
            self.layout.addWidget(self.acknowledge_lack_of_file)

            self.acknowledge_lack_of_file.clicked.connect(self.close)

    class FileSelection(QtWidgets.QFileDialog): #Selection box for input file
            def __init__(self):
                super().__init__()

                self.setWindowTitle("Choose a file")

    class OutputFileSelection(QtWidgets.QFileDialog): #Selection box for output file
            def __init__(self):
                super().__init__()

                self.setWindowTitle("Where to save file?")

    @QtCore.Slot()

    def about_clicked(self): #Open information window
        about_box = MainWindow.AboutProgram()
        about_box.resize(300,150)
        about_box.exec()

    def help_clicked(self):
        help_box = MainWindow.HelpWindow()
        help_box.resize(300,150)
        help_box.exec()

    def choose_file(self): #Choose input file
        if sys.platform == "win32":
            ffmpeg_input_file = MainWindow.FileSelection.getOpenFileName(self, 'Select a video file', os.path.expanduser("~\Videos"), 'Video files (*.mp4 *.mkv *.avi *.flv *.mov *webm)')
        elif sys.platform == "linux" or sys.platform == "darwin":
            ffmpeg_input_file = MainWindow.FileSelection.getOpenFileName(self, 'Select a video file', os.path.expanduser("~"), 'Video files (*.mp4 *.mkv *.avi *.flv *.mov *webm)')

        self.input_file.setText(str(ffmpeg_input_file[0]))

    def choose_where_output(self): #Choose output file
        if sys.platform == "win32":
            ffmpeg_output_file = MainWindow.OutputFileSelection.getSaveFileName(self, 'Select a video file', os.path.expanduser("~\Videos"), 'Video files (*.mp4 *.mkv *.mov)')
        elif sys.platform == "linux" or sys.platform == "darwin":
            ffmpeg_output_file = MainWindow.OutputFileSelection.getSaveFileName(self, 'Select a video file', os.path.expanduser("~"), 'Video files (*.mp4 *.mkv *.mov)')

        self.output_file.setText(str(ffmpeg_output_file[0]))

    def slider_updated(self): #Update the information text for sliders when the value changes.
        self.audio_bitrate_dialog.setText(f"Select the audio bitrate: {self.audio_bitrate.value()*32}")
        self.audio_bitrate_dialog.update()
        self.video_quality_text.setText(f"H264 quality setting: {self.video_quality.value()}")
        self.video_quality_text.update()
        self.thread_dialog.setText(f"Select the number of CPU threads to use: {self.threads.value()} / {os.cpu_count()}")
        self.thread_dialog.update()

    def go_button_clicked(self): #User clicked go
        
        ffmpeg_output_file = self.output_file.text()
        no_file_box = MainWindow.NoFileDialog()
        no_file_box.resize(200,120)

        if self.input_file.text() == "":
            no_file_box.exec()

        if os.path.exists(str(ffmpeg_output_file)):
            self.overwrite_existing_button.show()
            self.dont_overwrite_button.show()
            self.go_button.hide()

        else:
            self.run_ffmpeg()

    def overwrite_files(self): #User wants to overwrite existing file
        self.overwrite_existing_button.hide()
        self.dont_overwrite_button.hide()
        self.go_button.show()
        self.run_ffmpeg()

    def dont_overwrite_files(self): #User does NOT want to overwrite existing file
        self.overwrite_existing_button.hide()
        self.dont_overwrite_button.hide()
        self.go_button.show()

    def run_ffmpeg(self): #FFmpeg pre-run and commands

        progress = self.input_file.text() + '.tmp'
        if os.path.exists(progress):
            os.remove(progress)
        progress_file = open(progress, 'w')
        
        ffmpeg_input_file = self.input_file.text()
         
        #Get original resolution if not specified
        if self.resolution.text() == "":
            ffmpeg_res = "scale=" + subprocess.check_output([
                'ffprobe', '-v', 'error', '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height', '-of' 'csv=s=x:p=0', str(ffmpeg_input_file)
            ])
        else: #If there is text contained, use the user's given resolution
            ffmpeg_res = "scale=" + self.resolution.text()
            
        ffmpeg_output_file = self.output_file.text()
        ffmpeg_crf = self.video_quality.value()
        ffmpeg_audio_bitrate = str(int(self.audio_bitrate.value()*32))+'k'
        ffmpeg_threading = self.threads.value()
        ffmpeg_audio_codec = self.audio_codec.currentIndex()
        ffmpeg_encoder_preset = self.encoder_preset.currentText()
        audio_codecs = ["aac", "libopus"]
        ffmpeg_audio_codec = audio_codecs[ffmpeg_audio_codec]
        finish_box = MainWindow.FinishDialog()
        finish_box.resize(160,80)
        self.cancel_button.show()
        self.progress_bar_text.show()
        self.go_button.hide()
        ffmpeg_run = subprocess.Popen ([
            ffmpeg_path, '-y', # if you would like to use your PATH's FFmpeg, remove the "./" from "./ffmpeg"
            '-i', ffmpeg_input_file,
            '-c:v', 'libx264',
            '-crf', str(ffmpeg_crf),
            '-c:a', str(ffmpeg_audio_codec),
            '-b:a', str(ffmpeg_audio_bitrate),
            '-vf', str(ffmpeg_res),
            '-preset', str(ffmpeg_encoder_preset),
            '-vbr', 'off',
            '-threads', str(ffmpeg_threading) if str(ffmpeg_threading) else '4',
            '-progress', '-', '-nostats',
            ffmpeg_output_file
            ], stdout=progress_file, stderr=progress_file)      

        def ffmpeg_wait(): #Wait for FFmpeg, before running what shows after

            self.ffmpeg_running = True
            ffmpeg_run.wait()

            self.ffmpeg_running = False
            finish_box.exec()
            self.cancel_button.hide()
            self.progress_bar_text.hide()
            self.go_button.show()
            os.remove(progress)

        def ffmpeg_terminate(): #Kill FFmpeg early
            if sys.platform == "win32": #kill on win32
                while ffmpeg_run.poll() is None:
                    ffmpeg_run.kill()
                    time.sleep(5)
                    ffmpeg_killed = True

            elif sys.platform == "linux" or sys.platform == "darwin": #kill on unix
                while ffmpeg_run.poll() is None:
                    ffmpeg_run.send_signal(signal.SIGINT)
                    time.sleep(5)
                    ffmpeg_killed = True

            if ffmpeg_killed == True: #remove unfished files
                os.remove(ffmpeg_output_file)
                ffmpeg_killed = False

        def progress_bar(iteration, total, length=12, fill="#", nullp="-"): #Progress bar
            filledLength = length * iteration // total
            bar = (fill*length)[:filledLength] + (nullp*(length - filledLength))
            command = f"[{bar}]"
            return command

        def watch_progress(): #For progress bar
            time.sleep(0.5)
            frames = subprocess.check_output([
                'ffprobe', '-v', 'error', '-select_streams', 'v:0',
                '-count_frames', '-show_entries', 'stream=nb_read_frames',
                '-print_format', 'csv', self.input_file.text()
            ])
            frames_total = frames.decode('utf-8').strip()
            frames_total = int("".join([val for val in frames_total if val.isnumeric()]))
            
            while (ffmpeg_run.poll() == None):
                progress_data = open(progress)
                progress_lines = progress_data.readlines()
                progress_data.close()
                if len(progress_lines) > 12:
                    progress_lines_final = [i.strip().split("=") for i in progress_lines[-12:]]
                    try:
                        progress_dictionary = {data[0]: data[1] for data in progress_lines_final}
                    except:
                        continue
                    progress_used_list = progress_bar(int(progress_dictionary['frame']), frames_total, 64, fill='.', nullp=' ')
                    #print(self.progress_bar_text.text())
                    self.progress_bar_text.setText(progress_used_list)
                progress_data.close()
                time.sleep(0.5)
                    
        self.cancel_button.clicked.connect(ffmpeg_terminate)
        wait_on_ffmpeg = threading.Thread(target=ffmpeg_wait)
        wait_on_ffmpeg.start()
        progress_thread = threading.Thread(target=watch_progress)
        progress_thread.start()

if __name__ == "__main__": #Launch the main-window on run
    app = QtWidgets.QApplication([])

    main_app_window = MainWindow()
    main_app_window.resize(640, 360)
    main_app_window.show()

    #load the stylesheet
    with open('style.qss', 'r') as style:
        _style = style.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec())
