import PySimpleGUI as sg

from Dango_Analyzer.window import crop, extract, image_conversion, random_choice, analyze, resize
from Dango_Analyzer.window.analyze_window import labeling


class GuiMain:
   sg.theme('BlueMono')

   def __init__(self) -> None:
      self.handler = {
          'random': random_choice.Random().main,
          'crop': crop.Crop().main,
          'extract': extract.Extract().main,
          "analyze": analyze.Analyze().main,
          "csv_edit": labeling.Labeling().main,
          "image_conversion": image_conversion.ImageConversion().main,
          "movie_resize": resize.Resize().main,
      }

   def setup(self):
      self.menu_bar = [["ファイル", ["終了"]]]
      self.layout = [[sg.Text('メニューを選択してください', size=(30, 1), )],
                     [sg.Button('動画のクロッピング', key='crop', size=(50, 2))],
                     [sg.Button('フレーム分割', key='extract', size=(50, 2))],
                     [sg.Button('画像ランダム抽出', key='random', size=(50, 2))],
                     [sg.Button('動画リサイズ', key='movie_resize', size=(50, 2))],
                     [sg.Button('動画解析メニュー', key='analyze', size=(50, 2))],
                     [sg.Button('画像変換', key='image_conversion', size=(50, 2))],
                     [sg.Button('閉じる', key='Exit')]]
      # self.layout.append(sg.MenuBar(self.menu_bar))

      self.window = sg.Window('解析ツール', self.layout, size=(800, 600), keep_on_top=True)

   def main(self):
      self.setup()
      while True:
         event, value = self.window.read()
         if event == "Exit":
            break
         function = self.handler[event]
         self.window.close()
         function()
         self.setup()
      self.window.close()
