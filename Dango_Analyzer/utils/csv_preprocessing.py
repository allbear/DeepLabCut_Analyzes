import csv
import pandas as pd


class CSVProcess:

   def __empty__(self) -> None:
      self.frames_num = []
      self.x = {}
      self.y = {}
      self.neighborhood = {}
      self.frames = {}
      self.legends = []

   def csv_reader(self, csv_path) -> list:
      data = []
      try:
         with open(csv_path)as f:
            stream = csv.reader(f)
            for i in stream:
               data.append(i)
      except FileNotFoundError:
         pass
      return data

   def pd_preprocessing(self, data):
      del data[0]
      del data[1]
      columns = data.pop(0)
      df = pd.DataFrame(data, columns=columns)
      df = df.drop("bodyparts", axis=1)
      col = df.columns.values
      self.frames_num = [i for i in range(len(df))]
      for i, column in enumerate(col):
         if i % 3 == 0:
            col[i] = col[i].replace(column, f"{column}_1")
         elif i % 3 == 1:
            col[i] = col[i].replace(column, f"{column}_2")
         else:
            col[i] = col[i].replace(column, f"{column}_3")

      for i, column in enumerate(col):
         if i % 3 == 0:
            self.x[column.replace("_1", "")] = [float(j) for j in df[column]]
         elif i % 3 == 1:
            self.y[column.replace("_2", "")] = [float(j) for j in df[column]]
         else:
            self.neighborhood[column.replace("_3", "")] = [float(j) for j in df[column]]
            self.legends.append(column.replace("_3", ""))

   def preprocessing_frame(self):
      for i in self.frames_num:
         self.frames[str(i)] = {}
         for label in self.legends:
            self.frames[str(i)][label] = {"x": self.x[label][i], "y": self.y[label][i], "neighborhood": self.neighborhood[label][i]}

   def preprocessing(self, csv_path):
      self.__empty__()
      data: list = self.csv_reader(csv_path)
      if not data:
         return False
      else:
         self.pd_preprocessing(data)
         self.preprocessing_frame()
         return True
