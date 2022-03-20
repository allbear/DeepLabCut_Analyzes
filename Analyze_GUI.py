import json
import os
import time
import glob
import shutil
import random

import cv2
import pandas as pd
import PySimpleGUI as sg

import main


class Ui_Window():
   sg.theme('BlueMono')

   def setup(self):
      self.x = {}
      self.y = {}
      self.neighborhood = {}
      self.frames = []
      self.legends = []
      self.layout2 = []
      self.frame1 = sg.Frame('', [[sg.Text('読み取るCSVを選択してください')]])
      self.layout = [[sg.Text('読み取るCSVを選択してください')],
                     [sg.Text('ファイル', size=(15, 1)), sg.Input(), sg.FileBrowse('ファイルを選択', key='inputFilePath')],
                     [sg.Text('ファイル選択', size=(15, 1)), sg.Input(), sg.FileBrowse('ファイルを選択', key='input')],
                     [sg.Text('フレーム出力先', size=(15, 1)), sg.Input(), sg.FolderBrowse('保存フォルダを選択', key='output')],
                     [sg.Button('フレーム分割', key='cut'), sg.Checkbox("圧縮", key="compression_check", default=True), sg.Input('80', size=(3, 1), enable_events=True, key='compression')],
                     [sg.Text('', key="process")],
                     [sg.Button('画像ランダム抽出', key='random'), sg.Input('20', size=(4, 1), enable_events=True, key='random_num')],
                     [sg.Text('画像フォルダ選択', size=(15, 1)), sg.Input(), sg.FolderBrowse('フォルダを選択', key='random_input')],
                     [sg.Text('ランダム画像出力先', size=(15, 1)), sg.Input(), sg.FolderBrowse('保存フォルダを選択', key='random_output')],
                     [sg.Button('テスト', key='analyzes')],
                     [sg.Button('Exit')]]
      self.window = sg.Window('解析ツール', self.layout, size=(800, 600), keep_on_top=True)

   def pd_preprocessing(self, file_name):
      input_csv = pd.read_csv(file_name)
      df = input_csv.drop("bodyparts", axis=1)  # 余分なセルを削除
      columns = df.columns.values
      self.frames = [i for i in range(len(df))]
      for i, column in enumerate(columns):
         if i % 3 == 0:
            self.x[column] = [float(j) for j in df[column]]
         elif i % 3 == 1:
            self.y[column.replace(".1", "")] = [float(j) for j in df[column]]
         else:
            self.neighborhood[column.replace(".2", "")] = [float(j) for j in df[column]]
            self.legends.append(column.replace(".2", ""))

   def frame_extract(self, num, folder, ext="jpg"):
      files = glob.glob(f"{folder}/*.{ext}")
      files = random.sample(files, num)
      for f in files:
         if not os.path.exists("random_images"):
            os.mkdir()
         shutil.copy2(f, "random_images/")

   def flame_cut(self, input, output, compression_check, compression_parameter):
      cap = cv2.VideoCapture(input)
      if not cap.isOpened():
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

   def display_main(self):
      check_box = []
      for i in self.legends:
         check_box.append([sg.Checkbox(i, default=True)])
      main_layout = [[sg.Text('読み取るCSVを選択してください')],
                     [sg.Text('ファイル', size=(15, 1)), sg.Input(), sg.FileBrowse('ファイルを選択', key='inputFilePath')],
                     [sg.Button('解析', key='analyzes'), sg.Button('pickleに保存', key='save')],
                     [sg.Button('Exit')],
                     [sg.Column(check_box, scrollable=True)]]
      window = sg.Window("メイン画面", main_layout, size=(800, 800))
      while True:  # Event Loop
         event, values = window.read()
         if event in (sg.WIN_CLOSED, 'Exit'):
            print(values)
            return True
         if event == "analyzes":
            print("解析")
         if event == "save":
            self.pd_preprocessing(values['inputFilePath'])
            window.close()
            self.display_main()

   def main(self):
      self.setup()
      while True:
         event, values = self.window.read()
         if event in (sg.WIN_CLOSED, 'Exit'):
            break
         if event == "analyzes":
            main.pd_preprocessing(values['inputFilePath'])
         if event == "random":
            self.frame_extract(int(values['random_num']), values["random_input"])
         if event == "cut":
            self.flame_cut(values['input'], values['output'], values["compression_check"], int(values["compression"]))
         if event == "save":
            self.pd_preprocessing(values['inputFilePath'])
            self.window.close()
            dis = self.display_main()
            if dis is True:
               break

      self.window.close()


if __name__ == "__main__":
   ui = Ui_Window()
   ui.main()
