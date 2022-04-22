from GUI_MAIN import GuiMain


class Main:
   def __init__(self) -> None:
      super().__init__()
      self.path = "dango24"
      self.file_name = f"static/csv/{self.path}.csv"
      self.frames = {}

   def pd_preprocessing(self, datas):
      # if csv_file is None:
      #    input_csv = pd.read_csv(self.file_name)
      # else:
      #    input_csv = pd.read_csv(csv_file)
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

   def main(self):
      # data = self.csv_reader(self.file_name)
      # data = self.preprocessing(data)
      # self.pd_preprocessing()
      # self.preprocessing_frame()
      GuiMain().main()


if __name__ == "__main__":
   analayze = Main()
   analayze.main()
