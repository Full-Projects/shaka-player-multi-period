from decimal import Decimal
from bs4 import BeautifulSoup
import subprocess
import json
import os
import glob

class PrecisePeriodMPDProducer():
    input_filename = None
    output_mpd_filename = None
    filename_without_extension = None

    def __init__(self, input_filename, output_mpd_filename):
        self.input_filename = input_filename
        self.output_mpd_filename = output_mpd_filename
        self.filename_without_extension = os.path.splitext(self.input_filename)[0]
    
    def split_video(self, duration=10):
        _, extension = os.path.splitext(self.input_filename)
        if extension.lower() != '.mp4':
            print(f"The file {self.input_filename} is not an .mp4 file.")
            return
        command = f"ffmpeg -i {self.input_filename} -c copy -map 0 -segment_time {duration} -f segment {self.filename_without_extension}_%03d.mp4"  
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        out, err = process.communicate()
        if process.returncode != 0:
            print( f"The split_video command failed with return code: {process.returncode}")
    
    def get_target_files(self):
        return [f for f in glob.glob("*.mp4") if '_dashinit' not in f and f != self.input_filename]

    def generate_mpd_file(self, dash_duration=10000):
        files_list = self.get_target_files()
        command = "MP4Box" +   f" -dash {dash_duration}"
        for i, file in enumerate(files_list):
            command += f" {file}:period={i}"
        command += f" -out {self.output_mpd_filename}"
        
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        out, err = process.communicate()
        if process.returncode != 0:
            print( f"The generate_mpd_file command failed with return code: {process.returncode}")
        
        print("The command was used to create an MPD file: \n" + command ) 

    def convert_seconds_to_mpd_format(self, seconds):
        minutes, seconds = divmod(Decimal(seconds), 60)
        hours, minutes = divmod(minutes, 60)
        mpd_duration = "PT{}H{}M{}S".format(int(hours), int(minutes), seconds)
        return mpd_duration

    def get_video_duration(self, filename):
        command = f"ffprobe -v quiet -print_format json -show_format -show_streams {filename}"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        output_dict = json.loads(out)
        return Decimal(output_dict['streams'][0]['duration'])

    def execute(self):
        self.split_video(duration=10)
        self.generate_mpd_file(dash_duration=10000)
        with open(f'./{self.output_mpd_filename}', 'r') as mpd_file:
            mpd_data = mpd_file.read()
        soup = BeautifulSoup(mpd_data, 'xml')
        periods = soup.find_all('Period')
        total_video_duration = 0
        for i, period in enumerate(periods):
            base_url = period.find('BaseURL')  
            file_path = os.path.abspath(str(base_url.text).replace("_dashinit",""))
            video_duration = self.get_video_duration(file_path)
            total_video_duration += video_duration
            #print("\n\n" + period.get('duration') + " actual duration: " + str(video_duration) + "\n")
            period['duration'] = self.convert_seconds_to_mpd_format(video_duration) # seconds in ISO 8601 duration format
        #print("Total video duration: " + str(total_video_duration))
        mpd_file.close()
        #print("Total video duration in MPD Format: " + self.convert_seconds_to_mpd_format(total_video_duration))
        with open(f'./{self.output_mpd_filename}', 'w') as mpd_file:
            mpd_file.write(str(soup))

if __name__ == '__main__':
    video_splitter = PrecisePeriodMPDProducer("input.mp4","out.mpd")
    video_splitter.execute()
