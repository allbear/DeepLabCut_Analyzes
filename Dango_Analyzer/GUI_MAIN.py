import PySimpleGUI as sg

from Dango_Analyzer.windows import labeling, crop, extract, random_choice


class GuiMain:
   sg.theme('BlueMono')

   def __init__(self) -> None:
      self.handler = {
          'random': random_choice.Random().main,
          'crop': crop.Crop().main,
          'extract': extract.Extract().main,
          "labeling": labeling.Labeling().main
      }

   def setup(self):
      self.layout = [[sg.Text('メニューを選択してください', size=(15, 1), )],
                     [sg.Button('ラベリング', key='labeling', size=(50, 2))],
                     [sg.Button('動画のクロッピング', key='crop', size=(50, 2))],
                     [sg.Button('フレーム分割', key='extract', size=(50, 2))],
                     [sg.Button('画像ランダム抽出', key='random', size=(50, 2))],
                     [sg.Button('Exit', key="Exit")]]

      self.window = sg.Window('解析ツール', self.layout, size=(800, 600), keep_on_top=True)

   def main(self):
      self.setup()
      while True:
         event, value = self.window.read()
         if event == "Exit":
            break
         function = self.handler[event]
         function()
      self.window.close()
