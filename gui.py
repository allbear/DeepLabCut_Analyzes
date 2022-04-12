import json
import os
import time
import glob
import random

import cv2
import pandas as pd
import PySimpleGUI as sg

x = {}
y = {}
neighborhood = {}
frames = []
legends = []
layout2 = []
sg.theme('BlueMono')


frame1 = sg.Frame('', [[sg.Text('読み取るCSVを選択してください')]])


layout = [[sg.Text('読み取るCSVを選択してください')],
          [sg.Text('ファイル', size=(15, 1)), sg.Input(), sg.FileBrowse('ファイルを選択', key='inputFilePath')],
          [sg.Text('ファイル選択', size=(15, 1)), sg.Input(), sg.FileBrowse('ファイルを選択', key='input')],
          [sg.Text('フレーム出力先', size=(15, 1)), sg.Input(), sg.FolderBrowse('保存フォルダを選択', key='output')],
          [sg.Button('フレーム分割', key='cut'), sg.Checkbox("圧縮", key="compression_check", default=True), sg.Input('80', size=(3, 1), enable_events=True, key='compression')],
          [sg.Text('', key="process")],
          [sg.Button('画像ランダム抽出', key='random'), sg.Input('20', size=(4, 1), enable_events=True, key='random_num')],
          [sg.Text('画像フォルダ選択', size=(15, 1)), sg.Input(), sg.FolderBrowse('フォルダを選択', key='input')],
          [sg.Text('ランダム画像出力先', size=(15, 1)), sg.Input(), sg.FolderBrowse('保存フォルダを選択', key='output')],
          [sg.Button('テスト', key='analyzes')],
          [sg.Button('Exit')]]
window = sg.Window('解析ツール', layout, size=(800, 300), keep_on_top=True)


def pd_preprocessing(file_name):
   input_csv = pd.read_csv(file_name)
   df = input_csv.drop("bodyparts", axis=1)  # 余分なセルを削除
   columns = df.columns.values
   frames = [i for i in range(len(df))]
   for i, column in enumerate(columns):
      if i % 3 == 0:
         x[column] = [float(j) for j in df[column]]
      elif i % 3 == 1:
         y[column.replace(".1", "")] = [float(j) for j in df[column]]
      else:
         neighborhood[column.replace(".2", "")] = [float(j) for j in df[column]]
         legends.append(column.replace(".2", ""))


def frame_extract():
   pass


def flame_cut(input, output, compression_check, compression_parameter):
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
         window["process"].update("切り出しが完了しました")
         return


def display_main():
   check_box = []
   for i in legends:
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
         pd_preprocessing(values['inputFilePath'])
         window.close()
         display_main()


while True:  # Event Loop
   event, values = window.read()
   if event in (sg.WIN_CLOSED, 'Exit'):
      break
   if event == "analyzes":
      print(window["compression"])
   if event == "random":
      frame_extract(int(values['random_num']))
   if event == "cut":
      flame_cut(values['input'], values['output'], values["compression_check"], int(values["compression"]))
   if event == "save":
      pd_preprocessing(values['inputFilePath'])
      window.close()
      dis = display_main()
      if dis is True:
         break

window.close()
