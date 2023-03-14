import glob
import os
import random

import cv2
import ffmpeg
import tqdm
from PIL import Image


class FrameProcess:

   def __init__(self) -> None:
      self.times = 0

   def frame_random(self, num, folder, ext):
      files = glob.glob(f"{folder}/*.png")
      files.extend(glob.glob(f"{folder}/*.jpg"))
      files = random.sample(files, num)
      if not os.path.exists(f"{folder}/random_images"):
         os.mkdir(f"{folder}/random_images")
      for f in files:
         f_name = os.path.splitext(os.path.basename(f))[0]
         im = Image.open(f)
         im.save(f"{folder}/random_images/{f_name}.{ext}")

   def video_trimming(self, input, start_x, start_y, w, h):
      stream = ffmpeg.input(input)
      stream = ffmpeg.crop(stream, start_x, start_y, w, h)
      output_file_str = input.split(".")
      output_file_name = output_file_str[0] + "_trimed." + output_file_str[1]
      stream = ffmpeg.output(stream, output_file_name)
      ffmpeg.run(stream, overwrite_output=True)

   def frame_extract(self, input):
      cap = cv2.VideoCapture(input)
      if not cap.isOpened():
         return None
      return cap

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

   def resize(self, input, target_resolution, original_resolution, file_name, window):
      cap = cv2.VideoCapture(input)
      width, height = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 動画のサイズを取得
      # 指定が無ければ取得したサイズを使用
      if original_resolution[0] == 0:
         original_resolution[0] = width
         original_resolution[1] = height
      # リサイズを動画のサイズに合わせる
      target_w = round(width / (original_resolution[0] / target_resolution[0]))
      target_h = round(height / (original_resolution[1] / target_resolution[1]))

      fps = cap.get(cv2.CAP_PROP_FPS)
      weight = 100 / int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 進行度を取得するための変数
      fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
      output_path = input.split(os.path.basename(input))[0]
      writer = cv2.VideoWriter(f"{output_path}/{file_name}.mp4", fourcc, fps, (target_w, target_h))
      process: int = 0
      print(target_w, target_h)
      while True:
         ret, frame = cap.read()
         if not ret:
            break
         frame = cv2.resize(frame, (target_w, target_h))
         writer.write(frame)
         process += weight
         window.update_bar(int(process))
      window.update_bar(100)
