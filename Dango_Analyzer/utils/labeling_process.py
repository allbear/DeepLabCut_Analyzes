import copy
import os

import cv2
import matplotlib.pyplot as plt
import cmapy
import tqdm


class LabelingProcess:

   def line_draw(self, img, label, i, frames):
      for start in label.line_start:
         for end in label.line_end:
            start_x = int(frames[str(i)][start]["x"])
            start_y = int(frames[str(i)][start]["y"])
            end_x = int(frames[str(i)][end]["x"])
            end_y = int(frames[str(i)][end]["y"])
            cv2.line(img, (start_x, start_y), (end_x, end_y), (0, 255, 255), thickness=4, lineType=cv2.LINE_AA)
      return img

   def labeling(self, all_legends, frames, label, movie_path, output):
      cap = cv2.VideoCapture(movie_path)
      frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
      fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
      output_path = movie_path.split(os.path.basename(movie_path))[0]
      video = cv2.VideoWriter(f"{output_path}{output}.mp4", fourcc, 30, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
      for i in tqdm.tqdm(range(frame_count)):
         ret, img = cap.read()
         if ret:
            for num, legend in enumerate(label.parts):
               number = all_legends.index(legend)
               # color = copy.copy(list(cm(number / len(all_legends), bytes=True)))
               # color.pop(3)
               # colors = (int(color[0]), int(color[1]), int(color[2]))
               rgb_color = cmapy.color('rainbow', num / len(all_legends), rgb_order=True)
               cv2.circle(img, (int(frames[str(i)][legend]["x"]), int(frames[str(i)][legend]["y"])), 15, rgb_color, thickness=-1)
            img = self.line_draw(img, label, i, frames)
            video.write(img)
