import simpleaudio
from glob import glob
import time

from variable import GOOGLE_DIR

def play_sound(soundfile):
  wav_obj = simpleaudio.WaveObject.from_wave_file(soundfile)
  play_obj = wav_obj.play()
  play_obj.wait_done()

def get_files(**target_dir):
  if "second_dir" not in target_dir.keys() or target_dir["second_dir"] == None:
    return glob("{first_dir}**/*.wav".format(first_dir=target_dir["first_dir"]), recursive=True)
  else:
    return glob("{first_dir}{second_dir}/*.wav".format(first_dir=target_dir["first_dir"], 
                  second_dir=target_dir["second_dir"])
                  , recursive=True)

if __name__ == "__main__":
  target_sound_files = get_files(first_dir=GOOGLE_DIR, second_dir="浴室暖房")
  if len(target_sound_files) > 0:
    for target_sound_file in target_sound_files:
      play_sound(target_sound_file)
      time.sleep(7)