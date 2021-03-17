import datetime
import pandas as pd
import time


class DataLogger():

    def __init__(self, data_dir="../../data/", 
                current_log_filename="current_log",
                ready_to_sync_filename_prefix="not_synched"):

        self.data_dir = data_dir
        self.current_log_file_path = data_dir + current_log_filename

        self.measurements = [
            "timestamp", "g-force_x", "g-force_y", "g-force_z",
            "orientation_roll", "orientation_pitch", "orientation_yaw",
            "position_latitude", "position_longitude"
        ]
        self.num_measurements = len(self.measurements)

    def log(self, sensor_data: dict):
        # sensor_data format:
        # {"sensor_type": [value1, value2, value3..], "sensor_type2", [value1, value2, ...]}
        # Log NULL for values not present in measurements, e.g. if "pos" is not
        # present in sensor_data then logg a NULL for all its values
        

        df = pd.DataFrame.from_dict(sensor_data)
        df = df.reindex(columns=self.measurements)
        
        df.to_csv(f'{self.current_log_file_path}/{datetime.datetime.now()}_{len(df.index)}',
                    header=False, index=False, na_rep="null")

        # check if file now has too many entries and if so move the contents to
        # not_synched file and clear the current logging file



if __name__ == "__main__":
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    dl = DataLogger()
    dl.log({
            "timestamp":[datetime.datetime.now(), datetime.datetime.now()-datetime.timedelta(0,2)], "g-force_x":[1, 2], "g-force_y":[-1, 0], "g-force_z":[0.5, 2.9],
            "orientation_roll":[-12, 2], "orientation_pitch":[2,0], "orientation_yaw":[5,2],
            "position_longitude":[10.406478, 10.406678], "position_latitude":[63.415083, 63.416083]
   })
