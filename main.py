import csv
from http.client import ImproperConnectionState
import json
import os
import math
import statistics
import time

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image

from glahp import Graph


class analyze(Graph):
   def __init__(self) -> None:
      super().__init__()
      self.path = "dango24"
      self.file_name = f"csv/{self.path}.csv"
      self.input_csv = None

   def csv_reader(self) -> list:
      with open(self.file_name)as f:
         stream = csv.reader(f)
         data = []
         for i in stream:
            data.append(i)
      return data

   def change_name(self, datas):
      for i, data in enumerate(datas[0][1:]):
         if i % 3 == 0:
            datas[0][i] = data + "_x"
         elif i % 3 == 1:
            datas[0][i] = data + "_y"
         else:
            datas[0][i] = data + "_neighborhood"

   def preprocessing(self, datas):
      del datas[0]
      del datas[1]
      # self.change_name(datas)
      with open(self.file_name, 'w', newline="") as f:
         writer = csv.writer(f)
         writer.writerows(datas)

   def json_writer(self):
      with open("util.json", "r")as f:
         dic = json.load(f)
      dic["dango24"] = self.legends
      with open("util.json", "w")as f:
         json.dump(dic, f, indent=3)

   def pd_preprocessing(self):
      self.input_csv = pd.read_csv(self.file_name)
      df = self.input_csv.drop("bodyparts", axis=1)  # 余分なセルを削除
      columns = df.columns.values
      self.frames = [i for i in range(len(df))]
      for i, column in enumerate(columns):
         if i % 3 == 0:
            self.x[column] = [float(j) for j in df[column]]
         elif i % 3 == 1:
            self.y[column.replace(".1", "")] = [float(j) for j in df[column]]
         else:
            self.neighborhood[column.replace(".2", "")] = [float(j) for j in df[column]]
            self.legends.append(column.replace(".2", ""))

   def speed(self):
      for s in self.legends:
         plt.figure()
         plt.xlabel("x[mm/frame]", size="large", color="green")
         plt.ylabel("y[quantity]", size="large", color="blue")
         plt.yscale('log')
         speed = []
         leg1x = self.x[s]
         leg1y = self.y[s]
         nextx = 0
         nexty = 0
         count = 0
         for (i, j) in zip(leg1x, leg1y):
            if nextx == 0 and nexty == 0:
               nextx = i
               nexty = j
            else:
               long = math.sqrt((nextx - i)**2 + (nexty - j)**2) * 0.025
               if long < 0.4:
                  speed.append(long)
                  nextx = i
                  nexty = j
               else:
                  self.x[s][count] = nextx
                  self.y[s][count] = nexty

            count += 1

         plt.hist(speed, range=(0, 3.0), bins=300, label=s)
         plt.vlines(statistics.median(speed), ymin=0, ymax=5000, colors="r", linestyles=":")
         plt.vlines(statistics.mean(speed), ymin=0, ymax=5000, colors="m", linestyles=":")
         plt.legend()
         try:
            plt.savefig(f"images/{self.path}/{s}_hist.png", dpi=500, bbox_inches='tight')
         except FileNotFoundError:
            os.mkdir(f"images/{self.path}")
            plt.savefig(f"images/{self.path}/{s}_hist.png", dpi=500, bbox_inches='tight')

   def getRD(self, x, y):
      r = math.sqrt(x**2 + y**2)
      rad = math.atan2(y, x)
      degree = math.degrees(rad)
      return r, degree

   def convert(self):
      for s in self.legends:
         leg1x = self.x[s]
         leg1y = self.y[s]
         for (i, j) in zip(leg1x, leg1y):
            print(self.getRD(i, j))

   def overlap(self):
      im = Image.open(f"images/{self.path}/dango.jpg")
      fig = plt.figure()
      with open("util.json", "r")as f:
         util = json.load(f)
      colors = util["rolylegs_colors"]
      legs = util["14legs_dactylus"]
      fig = plt.figure()
      ax = fig.add_subplot(1, 1, 1)
      for i, column in enumerate(legs):
         ax.scatter(self.x[column][0], self.y[column][0], s=100, alpha=0.5, c=colors[i], label=legs[i])
         ax.set_xlim(0, 1280)
         ax.set_ylim(0, 720)
         ax.invert_yaxis()
         ax.imshow(im, alpha=0.6)
      plt.xlabel("x[pixel]", size="large", color="green")
      plt.ylabel("y[pixel]", size="large", color="blue")
      plt.legend(loc='best',
                 bbox_to_anchor=(1, 1),
                 borderaxespad=0.,)
      date = int(time.time())
      try:
         plt.savefig(f"images/{self.path}/{date}.png", dpi=500, bbox_inches='tight')
      except FileNotFoundError:
         os.mkdir(f"images/{self.path}")
         plt.savefig(f"images/{self.path}/{date}.png", dpi=500, bbox_inches='tight')

   def main(self):
      data = self.csv_reader()
      if data[0][0] == "scorer":
         print("加工します")
         self.preprocessing(data)
      else:
         print("既に加工されています")
      self.pd_preprocessing()
      self.all_plot()


if __name__ == "__main__":
   Analayze = analyze()
   Analayze.main()
