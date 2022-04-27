import copy
import os

import cv2
import PySimpleGUI as sg
import tqdm
import matplotlib.pyplot as plt

from Dango_Analyzer.utils.csv_preprocessing import Analyze


class Labeling(Analyze):
   sg.theme('BlueMono')

   def select_csv(self):
      self.layout = [[sg.Text("任意の部位とラベリングを行う動画を選択してください")],
                     [sg.Text('CSVファイルを選択', size=(15, 1)), sg.Input(), sg.FileBrowse('ファイルを選択', key='inputCSV')],
                     [sg.Button('CSVを選択', key='csv')],
                     [sg.Button('閉じる', key="Exit")]]
      self.window = sg.Window("メイン画面", self.layout, size=(800, 600), keep_on_top=True)

   def setup(self):
      check_box = []
      for i in self.legends:
         check_box.append([sg.Checkbox(i, default=True, key=i)])
      self.layout = [[sg.Text("任意の部位とラベリングを行う動画を選択してください")],
                     [sg.Button('解析', key='analyzes')],
                     [sg.Input(), sg.FileBrowse('動画を選択', key='movie')],
                     [sg.Text("出力する動画のファイル名を指定"), sg.Input("labeling", key="file_name")],
                     [sg.Button('閉じる', key="Exit")],
                     [sg.Column(check_box, scrollable=True)]]
      self.window = sg.Window("メイン画面", self.layout, size=(800, 600), keep_on_top=True)

   def labeling(self, all_legends, labeling_legend, movie_path, output):
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

   def main(self):
      self.select_csv()
      while True:
         event, values = self.window.read()
         if event == "Exit":
            break
         if event == "csv":
            self.preprocessing(values["inputCSV"])
            self.window.Close()
            self.setup()
         if event == "analyzes":
            parts = []
            for select_legend in self.legends:
               if values[select_legend] is True:
                  parts.append(select_legend)
            self.labeling(self.legends, parts, values["movie"], values["file_name"])
      self.window.Close()
