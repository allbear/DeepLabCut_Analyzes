import PySimpleGUI as sg

from windows import labeling, crop,extract


class GuiMain:
   sg.theme('BlueMono')

   def setup(self):
      self.layout = [[sg.Text('メニューを選択してください')],
                     [sg.Button('ラベリング', key='labeling')],
                     [sg.Button('動画のクロッピング', key='crop')],
                     [sg.Text('動画ファイルを選択', size=(25, 1)), sg.Input(), sg.FileBrowse('ファイルを選択', key='input')],
                     [sg.Button('フレーム分割', key='extract')],
                     [sg.Button('画像ランダム抽出', key='random'), sg.Input('20', size=(4, 1), enable_events=True, key='random_num')],
                     [sg.Text('画像フォルダ選択', size=(15, 1)), sg.Input(), sg.FolderBrowse('フォルダを選択', key='random_input')],
                     [sg.Text('ランダム画像出力先', size=(15, 1)), sg.Input(), sg.FolderBrowse('保存フォルダを選択', key='random_output')],
                     [sg.Button('テスト', key='analyzes')],
                     [sg.Button('Exit')]]
      self.window = sg.Window('解析ツール', self.layout, size=(800, 600), keep_on_top=True)

   def main(self):
      self.setup()
      while True:
         event, values = self.window.read()
         if event in (sg.WIN_CLOSED, 'Exit'):
            break
         if event == "analyzes":
            self.pd_preprocessing(values['inputFilePath'])
         if event == "random":
            frame.frame_extract(int(values['random_num']), values["random_input"])
         if event == "crop":
            crop.Crop().main()
         if event == "extract":
            extract.Extract().main()
         if event == "labeling":
            lab = labeling.Labeling()
            lab.display_main(values['inputFilePath'])
            self.window.close()
            dis = self.display_main(values['inputFilePath'])
            if dis is True:
               break
         if event == "save":
            self.pd_preprocessing(values['inputFilePath'])
            self.window.close()
            dis = self.display_main(values['inputFilePath'])
            if dis is True:
               break

      self.window.close()


if __name__ == "__main__":
   ui = GuiMain()
   ui.main()
