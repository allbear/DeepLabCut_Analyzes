import PySimpleGUI as sg

from main import analyze
from frame_process import Frame_Process as frame


class Ui_Window(analyze, frame):
   sg.theme('BlueMono')

   def setup(self):
      self.x = {}
      self.y = {}
      self.neighborhood = {}
      self.legends = []
      self.layout2 = []
      self.frame1 = sg.Frame('', [[sg.Text('読み取るCSVを選択してください')]])
      self.layout = [[sg.Text('読み取るCSVを選択してください')],
                     [sg.Text('CSVファイルを選択', size=(15, 1)), sg.Input(), sg.FileBrowse('ファイルを選択', key='inputFilePath'), sg.Button('ラベリング', key='labeling')],
                     [sg.Text('動画ファイルを選択', size=(25, 1)), sg.Input(), sg.FileBrowse('ファイルを選択', key='input')],
                     [sg.Text('フレーム出力先', size=(15, 1)), sg.Input(), sg.FolderBrowse('保存フォルダを選択', key='output')],
                     [sg.Button('フレーム分割', key='cut'), sg.Checkbox("圧縮", key="compression_check", default=True), sg.Input('80', size=(3, 1), enable_events=True, key='compression')],
                     [sg.Text('', key="process")],
                     [sg.Button('動画のクロッピング', key='crop'), sg.Text('x座標'), sg.Input('0', size=(3, 1), enable_events=True, key='x'), sg.Text('y座標'), sg.Input('0', size=(3, 1), enable_events=True, key='y'), sg.Text('幅'), sg.Input('0', size=(3, 1), enable_events=True, key='w'), sg.Text('高さ'), sg.Input('0', size=(3, 1), enable_events=True, key='h')],
                     [sg.Button('画像ランダム抽出', key='random'), sg.Input('20', size=(4, 1), enable_events=True, key='random_num')],
                     [sg.Text('画像フォルダ選択', size=(15, 1)), sg.Input(), sg.FolderBrowse('フォルダを選択', key='random_input')],
                     [sg.Text('ランダム画像出力先', size=(15, 1)), sg.Input(), sg.FolderBrowse('保存フォルダを選択', key='random_output')],
                     [sg.Button('テスト', key='analyzes')],
                     [sg.Button('Exit')]]
      self.window = sg.Window('解析ツール', self.layout, size=(800, 600), keep_on_top=True)

   def display_main(self, csv_path):
      check_box = []
      for i in self.legends:
         check_box.append([sg.Checkbox(i, default=True, key=i)])
      main_layout = [[sg.Text("任意の部位とラベリングを行う動画を選択してください")],
                     [sg.Button('解析', key='analyzes')],
                     [sg.Input(), sg.FileBrowse('動画を選択', key='movie')],
                     [sg.Text("出力する動画のファイル名を指定"), sg.Input("labeling", key="file_name")],
                     [sg.Button('Exit')],
                     [sg.Column(check_box, scrollable=True)]]
      window = sg.Window("メイン画面", main_layout, size=(800, 800))
      while True:  # Event Loops
         event, values = window.read()
         if event in (sg.WIN_CLOSED, 'Exit'):
            return True
         if event == "analyzes":
            parts = []
            for select_legend in self.legends:
               if values[select_legend] is True:
                  parts.append(select_legend)
            data = self.csv_reader(csv_path)
            if data[0][0] == "scorer":
               print("加工します")
               self.preprocessing(data)
            else:
               print("既に加工されています")
            self.preprocessing_frame2(parts)
            self.labeling(parts, self.legends, values["movie"], values["file_name"])

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
            frame.video_trimming(values['input'], int(values['x']), int(values['y']), int(values['w']), int(values['h']))
         if event == "cut":
            frame.flame_save(values['input'], values['output'], values["compression_check"], int(values["compression"]))
         if event == "labeling":
            data = self.csv_reader(values['inputFilePath'])
            if data[0][0] == "scorer":
               self.preprocessing(data, values['inputFilePath'])
            self.pd_preprocessing(values['inputFilePath'])
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
   ui = Ui_Window()
   ui.main()
