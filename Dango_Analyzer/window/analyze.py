import PySimpleGUI as sg
from Dango_Analyzer.window.analyze_window import labeling, graph_make


class Analyze:
   sg.theme('BlueMono')

   def __init__(self) -> None:
      self.handler = {
          'labeling': labeling.Labeling().main,
          "make_graph": graph_make.GraphMake().main
      }

   def setup(self):
      self.layout = [[sg.Text('メニューを選択してください', size=(15, 1), )],
                     [sg.Button('ラベリング', key='labeling', size=(50, 2))],
                     [sg.Button('中点をラべリング', key='center_labeling', size=(50, 2))],
                     [sg.Button('グラフ作成', key='make_graph', size=(50, 2))],
                     [sg.Button('戻る', key="Exit")]]

      self.window = sg.Window('解析ツール', self.layout, size=(800, 600), keep_on_top=True)

   def main(self):
      self.setup()
      while True:  # Event Loops
         event, values = self.window.read()
         if event == 'Exit':
            break
         function = self.handler[event]
         function()
      self.window.Close()
