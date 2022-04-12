import json
import os
import time
import glob
import shutil
import random

import cv2
import pandas as pd
import PySimpleGUI as sg
import ffmpeg

from main import analyze


class Ui_Window(analyze):
   sg.theme('BlueMono')

   def setup(self):
      self.x = {}
      self.y = {}
      self.neighborhood = {}
      self.legends = []
      self.layout2 = []
      self.frame1 = sg.Frame('', [[sg.Text('読み取るCSVを選択してください')]])
      self.layout = [[sg.Text('読み取るCSVを選択してください')],
                     [sg.Text('CSVファイルを選択', size=(15, 1)), sg.Input(), sg.FileBrowse('ファイルを選択', key='inputFilePath'), sg.Button('ラベリング', key='labeling')],
                     [sg.Text('分割したい動画ファイルを選択', size=(25, 1)), sg.Input(), sg.FileBrowse('ファイルを選択', key='input')],
                     [sg.Text('フレーム出力先', size=(15, 1)), sg.Input(), sg.FolderBrowse('保存フォルダを選択', key='output')],
                     [sg.Button('フレーム分割', key='cut'), sg.Checkbox("圧縮", key="compression_check", default=True), sg.Input('80', size=(3, 1), enable_events=True, key='compression')],
                     [sg.Text('', key="process")],
                     [sg.Button('動画のクロッピング', key='crop'), sg.Text('x座標'), sg.Input('0', size=(3, 1), enable_events=True, key='x'), sg.Text('y座標'), sg.Input('0', size=(3, 1), enable_events=True, key='w'), sg.Text('幅'), sg.Input('0', size=(3, 1), enable_events=True, key='x'), sg.Text('高さ'), sg.Input('0', size=(3, 1), enable_events=True, key='h')],
                     [sg.Button('画像ランダム抽出', key='random'), sg.Input('20', size=(4, 1), enable_events=True, key='random_num')],
                     [sg.Text('画像フォルダ選択', size=(15, 1)), sg.Input(), sg.FolderBrowse('フォルダを選択', key='random_input')],
                     [sg.Text('ランダム画像出力先', size=(15, 1)), sg.Input(), sg.FolderBrowse('保存フォルダを選択', key='random_output')],
                     [sg.Button('テスト', key='analyzes')],
                     [sg.Button('Exit')]]
      self.window = sg.Window('解析ツール', self.layout, size=(800, 600), keep_on_top=True)

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

   def video_trimming(input, output, start_x, start_y, w, h):

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

   def display_main(self, csv_path):
      check_box = []
      for i in self.legends:
         check_box.append([sg.Checkbox(i, default=True, key=i)])
      main_layout = [[sg.Text("任意の部位とラベリングを行う動画を選択してください")],
                     [sg.Button('解析', key='analyzes')],
                     [sg.Input(), sg.FileBrowse('動画を選択', key='movie')],
                     [sg.Button('Exit')],
                     [sg.Column(check_box, scrollable=True)]]
      window = sg.Window("メイン画面", main_layout, size=(800, 800))
      while True:  # Event Loops
         event, values = window.read()
         if event in (sg.WIN_CLOSED, 'Exit'):
            return True
         if event == "analyzes":
            parts = []
            for select_legend in self.legends:
               if values[select_legend] is True:
                  parts.append(select_legend)
            data = self.csv_reader(csv_path)
            if data[0][0] == "scorer":
               print("加工します")
               self.preprocessing(data)
            else:
               print("既に加工されています")
            self.preprocessing_frame2(parts)
            self.labeling(parts, values["movie"])

   def main(self):
      self.setup()
      while True:
         event, values = self.window.read()
         if event in (sg.WIN_CLOSED, 'Exit'):
            break
         if event == "analyzes":
            self.pd_preprocessing(values['inputFilePath'])
         if event == "random":
            self.frame_extract(int(values['random_num']), values["random_input"])
         if event == "cut":
            self.flame_save(values['input'], values['output'], values["compression_check"], int(values["compression"]))
         if event == "labeling":
            self.pd_preprocessing(values['inputFilePath'])
            self.window.close()
            dis = self.display_main(values['inputFilePath'])
            if dis is True:
               break
         if event == "save":
            self.pd_preprocessing(values['inputFilePath'])
            self.window.close()
            dis = self.display_main(values['inputFilePath'])
            if dis is True:
               break

      self.window.close()


if __name__ == "__main__":
   ui = Ui_Window()
   ui.main()
