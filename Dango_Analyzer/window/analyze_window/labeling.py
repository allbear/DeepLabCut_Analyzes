import PySimpleGUI as sg
from Dango_Analyzer.utils import labeling_process
from Dango_Analyzer.utils.csv_preprocessing import CSVProcess


class LabelCheck:
   def __init__(self) -> None:
      self.parts = []
      self.line_start = []
      self.line_end = []


class Labeling(CSVProcess):
   sg.theme('BlueMono')

   def select_csv(self):
      self.layout = [[sg.Text("CSVを選択してください")],
                     [sg.Text('CSVファイルを選択', size=(15, 1)), sg.Input(), sg.FileBrowse('ファイルを選択', key='inputCSV', file_types=(("CSV", ".csv"),))],
                     [sg.Button('CSVを選択', key='csv')],
                     [sg.Button('閉じる', key="Exit")]]
      self.window = sg.Window("メイン画面", self.layout, size=(800, 600), keep_on_top=True)

   def setup(self):
      check_box = [[], [], []]
      for i in self.legends:
         check_box[0].append([sg.Checkbox(i, default=True, key=i)])
         check_box[1].append([sg.Checkbox(i, default=False, key=f"{i}.1")])
         check_box[2].append([sg.Checkbox(i, default=False, key=f"{i}.2")])

      frame_1 = sg.Frame('ラベリングするラベルを選択', [
          [sg.Column(check_box[0], scrollable=True)]
      ])
      frame_2 = sg.Frame('ラインの起点を選択', [
          [sg.Column(check_box[1], scrollable=True)]
      ])
      frame_3 = sg.Frame('ラインの終点を選択', [
          [sg.Column(check_box[2], scrollable=True)]
      ])

      self.layout = [[sg.Text("任意の部位とラベリングを行う動画を選択してください")],
                     [sg.Button('解析', key='analyzes')],
                     [sg.Input(), sg.FileBrowse('動画を選択', key='movie')],
                     [sg.Text("出力する動画のファイル名を指定"), sg.Input("labeling", key="file_name")],
                     [sg.Button('CVS再選択', key="csv_select")],
                     [frame_1, frame_2, frame_3],
                     [sg.Button('閉じる', key="Exit")]]
      self.window = sg.Window("メイン画面", self.layout, size=(800, 600), keep_on_top=True)

   def label_checking(self, values):
      label = LabelCheck()
      select = []
      select = [x for x in self.legends]
      select += [x + ".1" for x in self.legends]
      select += [x + ".2" for x in self.legends]

      for select_legend in select:
         if values[select_legend] is True and ".1" in select_legend:
            label.line_start.append(select_legend.replace(".1", ""))
         elif values[select_legend] is True and ".2" in select_legend:
            label.line_end.append(select_legend.replace(".2", ""))
         elif values[select_legend] is True:
            label.parts.append(select_legend)
      return label

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
            label = self.label_checking(values)
            labeling_process.LabelingProcess().labeling(self.legends, self.frames, label, values["movie"], values["file_name"])
         if event == "csv_select":
            self.window.Close()
            self.select_csv()
      self.window.Close()
