import copy
import os

import cv2
import tqdm
import matplotlib.pyplot as plt


class LabelingProcess:

   def labeling(self, all_legends, frames, labeling_legend, movie_path, output):
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
               cv2.circle(frame, (int(frames[str(i)][legend]["x"]), int(frames[str(i)][legend]["y"])), 15, colors, thickness=-1)
            video.write(frame)
