import PySimpleGUI as sg

from windows.utils import frame_process


class Crop:
   sg.theme('BlueMono')

   def setup(self):
      self.layout = [[sg.Text("クロップを行う動画を選択してください")],
                     [sg.Button('クロップ', key='crop')],
                     [sg.Input(), sg.FileBrowse('動画を選択', key='movie')],
                     [sg.Text('x座標'), sg.Input('0', size=(3, 1), enable_events=True, key='x'), sg.Text('y座標'), sg.Input('0', size=(3, 1), enable_events=True, key='y'), sg.Text('幅'), sg.Input('0', size=(3, 1), enable_events=True, key='w'), sg.Text('高さ'), sg.Input('0', size=(3, 1), enable_events=True, key='h')],
                     [sg.Text("出力する動画のファイル名を指定"), sg.Input("crop", key="file_name")],
                     [sg.Button('閉じる', key="Exit")]]
      self.window = sg.Window("メイン画面", self.layout, size=(800, 600), keep_on_top=True)

   def main(self):
      self.setup()
      while True:  # Event Loops
         event, values = self.window.read()
         if event == 'Exit':
            break
         if event == "crop":
            frame_process.FrameProcess().video_trimming(values['movie'], int(values['x']), int(values['y']), int(values['w']), int(values['h']))
      self.window.Close()
