import os
import glob
import shutil
import random
import copy

import cv2
import ffmpeg
import matplotlib.pyplot as plt
import tqdm


class Frame_Process:

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
      while True:
         ret, frame = cap.read()
         if ret:
            if compression_check is True:
               cv2.imwrite(f'{output}/{str(n).zfill(digit)}.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), compression_parameter])
               print(f"{round(n/totalframes*100,1)}%完了")
               n += 1
            else:
               cv2.imwrite(f'{output}/{str(n).zfill(digit)}.png', frame)
               print(f'{output}/{str(n).zfill(digit)}.png')
               n += 1
         else:
            self.window["process"].update("切り出しが完了しました")
            return

   def labeling(self, labeling_legend, movie_path, output):
      cm = plt.cm.get_cmap("hsv", 256)
      cap = cv2.VideoCapture(movie_path)
      frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
      fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
      output_path = movie_path.split(os.path.basename(movie_path))[0]
      video = cv2.VideoWriter(f"{output_path}{output}.mp4", fourcc, 30, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
      for i in tqdm.tqdm(range(frame_count)):
         ret, frame = cap.read()
         if ret:
            for num, legend in enumerate(labeling_legend):
               color = copy.copy(list(cm(num / len(labeling_legend), bytes=True)))
               color.pop(3)
               colors = (int(color[0]), int(color[1]), int(color[2]))
               cv2.circle(frame, (int(self.frames[str(i)][legend]["x"]), int(self.frames[str(i)][legend]["y"])), 15, colors, thickness=-1)
            video.write(frame)
