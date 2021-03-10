import datetime
import pandas as pd


class DataLogger():

    def __init__(self, data_path="../../data/"):
        self.data_path = data_path

        self.measurements = ["g-force", "pos"]
        self.num_measurements = len(self.measurements)

    def log(self, sensor_data: dict):
        # sensor_data format:
        # {"sensor_type": [value1, value2, value3..], "sensor_type2", [value1, value2, ...]}
        # Log NULL for values not present in measurements, e.g. if "pos" is not
        # present in sensor_data then logg a NULL for all its values

        df = pd.DataFrame.from_dict(sensor_data)
        df = df.reindex(columns=self.measurements)
        df.to_csv(f'{self.data_path}{datetime.datetime.now()}_{len(df.index)}', header=False, index=False,
                  na_rep="null")


if __name__ == "__main__":
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    dl = DataLogger()
    dl.log({"pos": [1, 2, 3, 4, None], "g-force": [-1, -2, -3, -4, 1]})
