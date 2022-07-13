import PySimpleGUI as sg
from Dango_Analyzer.utils import labeling_process
from Dango_Analyzer.utils.csv_preprocessing import CSVProcess


class Labeling(CSVProcess):
   sg.theme('BlueMono')

   def select_csv(self):
      self.layout = [[sg.Text("CSVを選択してください")],
                     [sg.Text('CSVファイルを選択', size=(15, 1)), sg.Input(), sg.FileBrowse('ファイルを選択', key='inputCSV', file_types=(("CSV", ".csv"),))],
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
                     [sg.Button('CVS再選択', key="csv_select")],
                     [sg.Button('閉じる', key="Exit")],
                     [sg.Column(check_box, scrollable=True)]]
      self.window = sg.Window("メイン画面", self.layout, size=(800, 600), keep_on_top=True)

   def main(self):
      self.select_csv()
      while True:
         event, values = self.window.read()
         if event == "Exit":
            break
         if event == "csv":
            if self.preprocessing(values["inputCSV"]) is True:
               self.window.Close()
               self.setup()
            else:
               sg.popup('CSVファイルを選択してください', keep_on_top=True)
         if event == "analyzes":
            parts = []
            for select_legend in self.legends:
               if values[select_legend] is True:
                  parts.append(select_legend)
            labeling_process.LabelingProcess().labeling2(self.legends, self.frames, parts, values["movie"], values["file_name"])
         if event == "csv_select":
            self.window.Close()
            self.select_csv()
      self.window.Close()
