import PySimpleGUI as sg

from windows.utils import csv_preprocessing


class Labeling:
   sg.theme('BlueMono')

   def setup(self):
      check_box = []
      for i in self.legends:
         check_box.append([sg.Checkbox(i, default=True, key=i)])
      self.layout = [[sg.Text("任意の部位とラベリングを行う動画を選択してください")],
                     [sg.Button('解析', key='analyzes')],
                     [sg.Text('CSVファイルを選択', size=(15, 1)), sg.Input(), sg.FileBrowse('ファイルを選択', key='inputCSV')],
                     [sg.Input(), sg.FileBrowse('動画を選択', key='movie')],
                     [sg.Text("出力する動画のファイル名を指定"), sg.Input("labeling", key="file_name")],
                     [sg.Button('Exit')],
                     [sg.Column(check_box, scrollable=True)]]
      self.window = sg.Window("メイン画面", self.layout, size=(800, 800), keep_on_top=True)

   def display_main(self, csv_path):
      self.setup()
      while True:  # Event Loops
         event, values = self.window.read()
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
            self.labeling(parts, self.legends, values["movie"], values["file_name"])
