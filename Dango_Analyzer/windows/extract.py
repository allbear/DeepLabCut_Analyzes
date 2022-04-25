import PySimpleGUI as sg

from windows.utils import frame_process


class Extract:
   sg.theme('BlueMono')

   def setup(self):
      self.layout = [[sg.Text("フレーム抽出を行う動画を選択してください")],
                     [sg.Button('フレーム抽出', key='extract')],
                     [sg.Input(), sg.FileBrowse('動画を選択', key='movie')],
                     [sg.Text('フレーム出力先', size=(15, 1)), sg.Input(), sg.FolderBrowse('保存フォルダを選択', key='output')],
                     [sg.Checkbox("圧縮", key="compression_check", default=True), sg.Input('80', size=(3, 1), enable_events=True, key='compression')],
                     [sg.Text('', key="process")],
                     [sg.Button('メイン画面に戻る', key="back")],
                     [sg.Button('閉じる', key="Exit")]]
      self.window = sg.Window("フレーム抽出", self.layout, size=(800, 600), keep_on_top=True)

   def main(self):
      self.setup()
      while True:  # Event Loop
         event, values = self.window.read()
         if event == 'Exit':
            break
         if event == "extract":
            frame_process.FrameProcess().flame_save(values['movie'], values['output'], values["compression_check"], int(values["compression"]))
            self.window["process"].update("切り出しが完了しました")
      self.window.Close()
