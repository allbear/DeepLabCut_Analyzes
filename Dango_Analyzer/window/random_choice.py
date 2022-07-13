import PySimpleGUI as sg

from Dango_Analyzer.utils import frame_process


class Random:
   sg.theme('BlueMono')

   def setup(self):
      self.layout = [[sg.Text("フレーム抽出を行う動画を選択してください", key="process")],
                     [sg.Button('ランダム抽出', key='random')],
                     [sg.Input('20', size=(4, 1), enable_events=True, key='random_num')],
                     [sg.Radio(text='png', key="png", group_id='1', default=True)],
                     [sg.Radio(text='jpg', key="jpg", group_id='1', default=False)],
                     [sg.Text('出力先', size=(15, 1)), sg.Input(), sg.FolderBrowse('フレームのフォルダを選択', key='output')],
                     [sg.Button('閉じる', key="Exit")]]
      self.window = sg.Window("フレーム抽出", self.layout, size=(800, 600), keep_on_top=True)

   def main(self):
      self.setup()
      while True:
         event, values = self.window.read()
         if event == 'Exit':
            break
         if event == "random":
            self.window["process"].update("抜き出しを開始します")
            if values["png"] is True:
               pic_type = "png"
            else:
               pic_type = "jpg"
            frame_process.FrameProcess().frame_random(int(values['random_num']), values["output"], pic_type)
            self.window["process"].update("抜き出しが完了しました")
      self.window.Close()
