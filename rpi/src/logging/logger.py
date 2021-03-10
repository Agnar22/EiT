import datetime
import pandas as pd


class DataLogger():

    def __init__(self, data_dir="../../data/", 
                current_log_filename="current_log",
                ready_to_sync_filename_prefix="not_synched"):

        self.data_dir = data_dir
        self.current_log_file_path = data_dir + current_log_filename

        self.measurements = ["timestamp", "g-force", "orientation", "position"]
        self.num_measurements = len(self.measurements)

    def log(self, sensor_data: dict):
        # sensor_data format:
        # {"sensor_type": [value1, value2, value3..], "sensor_type2", [value1, value2, ...]}
        # Log NULL for values not present in measurements, e.g. if "pos" is not
        # present in sensor_data then logg a NULL for all its values
        

        df = pd.DataFrame.from_dict(sensor_data)
        df = df.reindex(columns=self.measurements)
        
        df.to_csv(f'{self.current_log_file_path} \
                    {datetime.datetime.now()}_{len(df.index)}',
                    header=False, index=False, na_rep="null")

        # check if file now has too many entries and if so move the contents to
        # not_synched file and clear the current logging file



if __name__ == "__main__":
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    dl = DataLogger()
    dl.log({"pos": [1, 2, 3, 4, None], "g-force": [-1, -2, -3, -4, 1]})
