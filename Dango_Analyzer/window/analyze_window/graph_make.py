import cv2
import PySimpleGUI as sg
from Dango_Analyzer.utils import graph
from Dango_Analyzer.utils.csv_preprocessing import CSVProcess


class GraphMake(CSVProcess):
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
      self.layout = [[sg.Text("任意の部位を選択してください")],
                     [sg.Button('グラフ作成', key='_glaph_')],
                     [sg.Input(), sg.FileBrowse('動画を選択', key='movie')],
                     [sg.Text("出力するグラフのファイル名を指定"), sg.Input("labeling", key="file_name")],
                     [sg.Text("尤度を選択してください")],
                     [sg.Input("0.4", key="likelihood", size=(3, 1))],
                     [sg.Button('CVS再選択', key="csv_select")],
                     [sg.Button('閉じる', key="Exit")],
                     [sg.Column(check_box, scrollable=True)]]
      self.window = sg.Window("メイン画面", self.layout, size=(800, 600), keep_on_top=True)

   def get_movie_property(self, path):
      video = cv2.VideoCapture(path)
      width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
      heigth = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
      return width, heigth

   def main(self):
      self.select_csv()
      while True:
         event, values = self.window.read()
         if event == "Exit":
            break
         if event == "csv":
            csv_path = values["inputCSV"]
            if self.preprocessing(csv_path) is True:
               self.window.Close()
               self.setup()
            else:
               sg.popup('CSVファイルを選択してください', keep_on_top=True)
         if event == "_glaph_":
            parts = []
            for select_legend in self.legends:
               if values[select_legend] is True:
                  parts.append(select_legend)
            width, height = self.get_movie_property(values["movie"])
            graph.Graph().all_body_plot(csv_path, values["file_name"], parts, width, height, float(values["likelihood"]))
         if event == "csv_select":
            self.window.Close()
            self.select_csv()
      self.window.Close()
