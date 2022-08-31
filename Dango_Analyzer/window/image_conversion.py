import io

import cv2
import PySimpleGUI as sg
from PIL import Image


class ImageConversion:
   sg.theme('BlueMono')

   def setup(self):
      self.layout = [[sg.Text("画像を選択してください")],
                     [sg.Button('再生', key='play')],
                     [sg.Input(), sg.FileBrowse('画像を選択', key='image_path')],
                     [sg.Image("", key="_Image_")],
                     [sg.Button('閉じる', key="Exit", pad=((1400, 0), (800, 0)))]]
      self.window = sg.Window("メイン画面", self.layout, size=(1500, 1000))

   def get_image(self, path):
      image = Image.open(path)
      if image.width > 1500 / 2:
         image.thumbnail(size=(750, 750))
      bio = io.BytesIO()
      image.save(bio, format="PNG")
      self.window["_Image_"].update(data=bio.getvalue())

   def main(self):
      self.setup()
      while True:
         event, values = self.window.read()
         if event == 'Exit':
            break
         if event == "play":
            self.get_image(values["image_path"])

      self.window.Close()
