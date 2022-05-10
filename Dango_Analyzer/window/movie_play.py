import PySimpleGUI as sg

import cv2


class Movie:
   sg.theme('BlueMono')

   def setup(self):
      self.layout = [[sg.Text("再生する動画を選択してください")],
                     [sg.Button('再生', key='play')],
                     [sg.Button('画像表示', key='image')],
                     [sg.Input(), sg.FileBrowse('動画を選択', key='movie')],
                     [sg.Image(filename='', key='image')],
                     [sg.Button('閉じる', key="Exit")]]
      self.window = sg.Window("メイン画面", self.layout, location=(0, 0), keep_on_top=True)

   # def play(self, path):
   #    cap = cv2.VideoCapture(path)
   #    while cap.isOpened():
   #       _, frame = cap.read()
   #       imgbytes = cv2.imencode('.png', frame)[1].tobytes()
   #       self.window['image'].update(data=imgbytes)
   #       if cv2.waitKey(25) & 0xFF == ord('q'):
   #          break

   def main(self):
      self.setup()
      flag = False
      while True:
         event, values = self.window.read()
         if event == 'Exit':
            break
         if event == "play":
            flag = True
         if flag is True:
            cap = cv2.VideoCapture(values["movie"])
            while cap.isOpened():
               _, frame = cap.read()
               imgbytes = cv2.imencode('.png', frame)[1].tobytes()
               self.window['image'].update(data=imgbytes)
               if cv2.waitKey(25) & 0xFF == ord('q'):
                  break
      self.window.Close()
