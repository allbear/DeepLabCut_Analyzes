import csv
import pandas as pd


class Analyze:

   def csv_reader(self, csv_path) -> list:
      with open(csv_path)as f:
         stream = csv.reader(f)
         data = []
         for i in stream:
            data.append(i)
      return data

   def preprocessing(self, datas, csv_path):
      del datas[0]
      del datas[1]
      return datas

   def pd_preprocessing(self, datas):
      df = pd.DataFrame(datas)
      df = df.drop("bodyparts", axis=1)  # 余分なセルを削除
      columns = df.columns.values
      self.frames_num = [i for i in range(len(df))]
      for i, column in enumerate(columns):
         if i % 3 == 0:
            self.x[column] = [float(j) for j in df[column]]
         elif i % 3 == 1:
            self.y[column.replace(".1", "")] = [float(j) for j in df[column]]
         else:
            self.neighborhood[column.replace(".2", "")] = [float(j) for j in df[column]]
            self.legends.append(column.replace(".2", ""))

   def preprocessing_frame(self):
      for i in self.frames_num:
         self.frames[str(i)] = {}
         for label in self.legends:
            self.frames[str(i)][label] = {"x": self.x[label][i], "y": self.y[label][i], "neighborhood": self.neighborhood[label][i]}
