import PySimpleGUI as sg
from datetime import datetime
import time


class LearningTime:
   sg.theme('BlueMono')

   def __init__(self) -> None:
      self.calc_flag = False

   def time_calc(self, log):
      timestamp = []
      with open(log, "r")as f:
         text = f.read().splitlines()
      for i in text:
         if "iteration:" in i:
            timestamp.append(i)
      timestamp[0].split(" ")[1]
      start = datetime.strptime(timestamp[0].split(" ")[0] + " " + timestamp[0].split(" ")[1], '%Y-%m-%d %H:%M:%S')
      late = datetime.strptime(timestamp[-1].split(" ")[0] + " " + timestamp[-1].split(" ")[1], '%Y-%m-%d %H:%M:%S')
      all_time = (late - start) / len(timestamp) * 5000
      nokori = all_time - (late - start)
      nokori = str(nokori).split(".")[0]
      return nokori

   # ログがたまるまで待機
   def log_confirmation(self, log):
      with open(log, "r")as f:
         text = f.read().splitlines()
      count = 0
      for i in text:
         if "iteration:" in i:
            count += 1
      return count


   def setup(self):
      self.layout = [[sg.Text("学習中のログファイルを選択してください")],
                     [sg.Button('残り時間を計算する', key='calc')],
                     [sg.Input(), sg.FileBrowse('ログファイルを選択', key='log_txt')],
                     [sg.Text('学習回数'), sg.Input(size=(7, 1), enable_events=True, key='learning_total'), sg.Text('display_iterations'), sg.Input(size=(7, 1), enable_events=True, key='display_iterations')],
                     [sg.Text("", font=('Noto Serif CJK JP', 30), key="_time_")],
                     [sg.Button('閉じる', key="Exit")],
                     [sg.Text("", font=('Noto Serif CJK JP', 100), key="_time2_")]]
      self.window = sg.Window("フレーム抽出", self.layout, size=(800, 600), keep_on_top=True)

   def main(self):
      self.setup()
      while True:  # Event Loop
         event, values = self.window.read(timeout=3000, timeout_key='_timeout_')
         if event == 'Exit':
            break

         if event == "calc":
            if values["log_txt"] != "":
               self.window['_time_'].update("計測を開始します。しばらくお待ちください")
               self.calc_flag = True
            else:
               self.window['_time_'].update("ファイルが選択されていません")

         if event == "_timeout_" and self.calc_flag is True:
            if self.log_confirmation(values["log_txt"]) < 3:
               self.window['_time_'].update("ログがたまるまでしばらくお待ちください")
               continue
            self.window['_time_'].update("残り学習時間を表示しています")
            nokori = self.time_calc(values["log_txt"])
            self.window['_time2_'].update(nokori)
            if nokori == "0:00:00":
                self.window['_time_'].update("学習が終了しました")

      self.window.Close()
