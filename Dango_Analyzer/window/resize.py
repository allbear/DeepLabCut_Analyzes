import PySimpleGUI as sg
from Dango_Analyzer.utils import frame_process


class Resize:
   sg.theme('BlueMono')

   def setup(self):
      size_list = [480, 640, 720, 800, 960, 1024, 1280, 1440, 1600, 1920, 2560]
      preview_size = [f"{str(x)}×{str(int(x*9/16))}" for x in size_list]
      self.resolutions = dict(zip(preview_size, size_list))
      self.layout = [[sg.Text("リサイズを行う動画を選択してください")],
                     [sg.Button('リサイズ', key='resize')],
                     [sg.ProgressBar(100, pad=((1.0), (0.0)), orientation="h", size=(15, 16), key="bar")],
                     [sg.Text("", key="resize_lavel")],
                     [sg.Input(), sg.FileBrowse('動画を選択', key='movie')],
                     [sg.Listbox(preview_size, size=(15, len(size_list)), key='_resize_')],
                     [sg.Text("出力する動画のファイル名を指定"), sg.Input("resize", key="file_name")],
                     [sg.Button('閉じる', key="Exit")]]
      self.window = sg.Window("メイン画面", self.layout, size=(800, 600), keep_on_top=True)

   def main(self):
      self.setup()
      while True:
         event, values = self.window.read()
         if event == 'Exit':
            break
         if event == "resize":
            self.window["resize_lavel"].update("処理中です")
            frame_process.FrameProcess().resize(values["movie"], self.resolutions[values["_resize_"][0]], values["file_name"], self.window["bar"])
            self.window["resize_lavel"].update("完了しました")
      self.window.Close()
