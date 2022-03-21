import csv
import json
import math
import os
import statistics
import time
from turtle import color

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.animation as animation


class Graph():
   def __init__(self) -> None:
      self.input_csv = None
      self.legends = []  # 凡例
      self.frames_num = []
      self.x = {}
      self.y = {}
      self.neighborhood = {}
      self.animation_x = {}
      self.animation_y = {}
      self.animation_frames = {}
      self.plots_data = []
      self.width = 2160
      self.height = 3840

   def plot(self):
      fig = plt.figure()
      with open("util.json", "r")as f:
         util = json.load(f)
      colors = util["rolylegs_colors"]
      legs = util["14legs_dactylus"]
      for i, column in enumerate(legs):
         fig = plt.figure()
         ax = fig.add_subplot(1, 1, 1)
         ax.scatter(self.x[column], self.y[column], s=30, alpha=0.5, c=colors[i], label=legs[i])
         ax.set_xlim(0, self.width)
         ax.set_ylim(0, self.height)
         ax.invert_yaxis()
         plt.xlabel("x[pixel]", size="large", color="green")
         plt.ylabel("y[pixel]", size="large", color="blue")
         plt.legend(loc='best',
                    bbox_to_anchor=(1, 1),
                    borderaxespad=0.,)
         try:
            plt.savefig(f"images/{self.path}/{column}.png", dpi=500, bbox_inches='tight')
         except FileNotFoundError:
            os.mkdir(f"images/{self.path}")
            plt.savefig(f"images/{self.path}/{column}.png", dpi=500, bbox_inches='tight')

   def all_plot(self):  # すべての指定のパーツをプロット
      fig = plt.figure()
      with open("util.json", "r")as f:
         util = json.load(f)
      colors = util["rolylegs_colors"]
      parts = util["14legs_dactylus"]
      fig = plt.figure()
      ax = fig.add_subplot(1, 1, 1, aspect="equal")
      for i, column in enumerate(parts):
         ax.scatter(self.x[column], self.y[column], s=30, alpha=0.5, c=colors[i], label=column)
         ax.set_xlim(0, self.width)
         ax.set_ylim(0, self.height)
         ax.invert_yaxis()
      plt.xlabel("x[pixel]", size="large", color="green")
      plt.ylabel("y[pixel]", size="large", color="blue")
      plt.legend(loc='best', bbox_to_anchor=(1, 1), handletextpad=0.3, borderaxespad=0, borderpad=0)
      try:
         plt.savefig(f"images/{self.path}/{self.path}.png", dpi=500, bbox_inches='tight')
      except FileNotFoundError:
         os.mkdir(f"images/{self.path}")
         plt.savefig(f"images/{self.path}/{self.path}.png", dpi=500, bbox_inches='tight')

   def all_body_plot(self):  # すべてのパーツをプロット
      fig = plt.figure()
      ax = fig.add_subplot(1, 1, 1, aspect="equal")
      for i, column in enumerate(self.legends):
         ax.scatter(self.x[column], self.y[column], s=30, alpha=0.5, label=column)
         ax.set_xlim(0, self.width)
         ax.set_ylim(0, self.height)
         ax.invert_yaxis()
         plt.xlabel("x[pixel]", size="large", color="green")
         plt.ylabel("y[pixel]", size="large", color="blue")
         plt.legend(loc='best',
                    bbox_to_anchor=(1, 1),
                    borderaxespad=0.,)
      try:
         plt.savefig(f"images/{self.path}/total.png", dpi=500, bbox_inches='tight')
      except FileNotFoundError:
         os.mkdir(f"images/{self.path}")
         plt.savefig(f"images/{self.path}/total.png", dpi=500, bbox_inches='tight')

   def frame_x_y(self, ax, colors, legs, part):
      if part == 1:
         for i, column in enumerate(legs[0:7]):
            ax.plot(self.frames_num, self.x[column], linewidth=2, c=colors[i], label=column + "_x")
         for i, column in enumerate(legs[0:7]):
            ax.plot(self.frames_num, self.y[column], linewidth=2, c=colors[i], linestyle="dashed", label=column + "_y")
      else:
         for i, column in enumerate(legs[7:14]):
            ax.plot(self.frames_num, self.x[column], linewidth=2, c=colors[i + 7], label=column + "_x")
         for i, column in enumerate(legs[7:14]):
            ax.plot(self.frames_num, self.y[column], linewidth=2, c=colors[i + 7], linestyle="dashed", label=column + "_y")
      return ax

   def frame_x_y2(self, ax, colors, legs, part, num):
      self.plots_data.append(self.frames_num[num])
      if part == 1:
         for i, column in enumerate(legs[0:7]):
            if column not in self.animation_x:
               self.animation_x[column] = self.x[column][0:num + 1]
            else:
               self.animation_x[column].append(self.x[column][0:num + 1])
            print(self.plots_data, self.animation_x[column])
            ax.plot(self.plots_data, self.animation_x[column], linewidth=2, c=colors[i], label=column + "_x")
         for i, column in enumerate(legs[0:7]):
            if column not in self.animation_y:
               self.animation_y[column] = self.y[column][0:num + 1]
            else:
               self.animation_y[column].append(self.y[column][0:num + 1])
            ax.plot(self.plots_data, self.animation_y[column], linewidth=2, c=colors[i], label=column + "_x")
      else:
         for i, column in enumerate(legs[7:14]):
            ax.plot([self.frames_num[num]], [self.x[column][num]], linewidth=2, c=colors[i + 7], label=column + "_x")
         for i, column in enumerate(legs[7:14]):
            ax.plot([self.frames_num[num]], [self.y[column][num]], linewidth=2, c=colors[i + 7], linestyle="dashed", label=column + "_y")
      return ax

   def frame_plot(self):
      fig = plt.figure()
      plt.rcParams['figure.figsize'] = (20, 5)
      with open("util.json", "r")as f:
         util = json.load(f)
      colors = util["rolylegs_colors"]
      legs = util["14legs_dactylus"]
      ax = fig.add_subplot(1, 1, 1)
      ax.set_xlim(0, 10000)
      ax.set_ylim(0, 1280)
      part = 2
      ax = self.frame_x_y(ax, colors, legs, part)
      plt.xlabel("Frame Index", size="large", color="green")
      plt.ylabel("x(soild),y(dashed)[pixel]", size="large", color="blue")
      plt.legend(loc='best',
                 bbox_to_anchor=(1, 1),
                 borderaxespad=0.,)
      try:
         plt.savefig(f"images/{self.path}/{self.path}_frame{part}.png", dpi=500, bbox_inches='tight')
      except FileNotFoundError:
         os.mkdir(f"images/{self.path}")
         plt.savefig(f"images/{self.path}/{self.path}_frame{part}.png", dpi=500, bbox_inches='tight')

   def midi(self):
      im = Image.open(f"images/{self.path}/haimen.jpg")
      fig = plt.figure()
      with open("util.json", "r")as f:
         dic = json.load(f)
      haimen = dic["haimen_dango"]
      colors = dic["rolylegs_colors"]
      ax = fig.add_subplot(1, 1, 1)
      ax.imshow(im, alpha=0.6)
      ax.set_xlim(0, 2160)
      ax.set_ylim(0, 3840)
      cen_x = (self.x["tail"][0] + self.x["head"][0]) / 2
      cen_y = (self.y["tail"][0] + self.y["head"][0]) / 2
      ax.scatter(self.x["head"][0], self.y["head"][0], s=30, alpha=0.5, c="blue", label="head")
      ax.scatter(self.x["tail"][0], self.y["tail"][0], s=30, alpha=0.5, c="blue", label="tail")
      ax.scatter(cen_x, cen_y, s=30, alpha=0.5, c="blue", label="center")
      plt.xlabel("Frame Index", size="large", color="green")
      plt.ylabel("x(soild),y(dashed)[pixel]", size="large", color="blue")
      plt.legend(loc='best',
                 bbox_to_anchor=(1, 1),
                 borderaxespad=0.,)
      try:
         plt.savefig(f"images/{self.path}/{self.path}_frame.png", dpi=500, bbox_inches='tight')
      except FileNotFoundError:
         os.mkdir(f"images/{self.path}")
         plt.savefig(f"images/{self.path}/{self.path}_frame.png", dpi=500, bbox_inches='tight')

   def frame_plot2(self):
      fig = plt.figure()
      plt.rcParams['figure.figsize'] = (20, 5)
      with open("util.json", "r")as f:
         util = json.load(f)
      colors = util["rolylegs_colors"]
      legs = util["14legs_dactylus"]

      for i in range(len(self.frames_num)):
         fig = plt.figure()
         ax = fig.add_subplot(1, 1, 1)
         ax.set_xlim(0, 10000)
         ax.set_ylim(0, 1280)
         part = 1
         ax = self.frame_x_y2(ax, colors, legs, part, i)
         plt.xlabel("Frame Index", size="large", color="green")
         plt.ylabel("x(soild),y(dashed)[pixel]", size="large", color="blue")
         plt.legend(loc='best',
                    bbox_to_anchor=(1, 1),
                    borderaxespad=0.,)
         try:
            plt.savefig(f"images/{self.path}/{self.path}flames/{self.path}_frame{i}.png", dpi=500, bbox_inches='tight')
         except FileNotFoundError:
            os.mkdir(f"images/{self.path}/{self.path}flames")
            plt.savefig(f"images/{self.path}/{self.path}flames/{self.path}_frame{i}.png", dpi=500, bbox_inches='tight')


if __name__ == "__main__":
   Analayze = Graph()
   Analayze.main()
