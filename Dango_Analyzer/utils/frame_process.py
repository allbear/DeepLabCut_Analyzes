import os
import glob
import shutil
import random
import copy

import cv2
import ffmpeg
import matplotlib.pyplot as plt
import tqdm


class FrameProcess:

   def __init__(self) -> None:
      self.times = 0

   def frame_extract2(self, num, folder, ext="jpg"):
      files = glob.glob(f"{folder}/*.{ext}")
      files = random.sample(files, num)
      for f in files:
         if not os.path.exists(f"{folder}/random_images"):
            os.mkdir()
         shutil.copy2(f, f"{folder}/random_images")

   def frame_extract(self, input):
      cap = cv2.VideoCapture(input)
      if not cap.isOpened():
         return None
      return cap

   def video_trimming(self, input, start_x, start_y, w, h):
      stream = ffmpeg.input(input)
      stream = ffmpeg.crop(stream, start_x, start_y, w, h)
      output_file_str = input.split(".")
      output_file_name = output_file_str[0] + "_trimed." + output_file_str[1]
      stream = ffmpeg.output(stream, output_file_name)
      ffmpeg.run(stream, overwrite_output=True)

   def flame_save(self, input, output, compression_check, compression_parameter):
      cap = self.frame_extract(input)
      if cap is None:
         return
      digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
      n = 0
      totalframes = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
      for i in tqdm.tqdm(range(totalframes)):
         ret, frame = cap.read()
         if ret:
            if compression_check is True:
               cv2.imwrite(f'{output}/{str(n).zfill(digit)}.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), compression_parameter])
               n += 1
            else:
               cv2.imwrite(f'{output}/{str(n).zfill(digit)}.png', frame)
               n += 1
