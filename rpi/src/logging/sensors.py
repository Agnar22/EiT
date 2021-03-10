
from sense_hat import SenseHat
from queue import Queue
import time


class DataQueue():

    def __init__(self):
        self.queue = Queue()

    def put(self, data_type: str, data: list):
        queue_element = {"data_type": data_type, "data": data}
        self.queue.put(queue_element)


class SensorReader():

    def __init__(self):

        self.data_queue = Queue()
        self.sense = SenseHat()
        self.sense.set_imu_config(True, True, False)

    def read_gyro(self):
        while True:
            orientation = self.sense.get_orientation_degrees()
            print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))
            time.sleep(1)

    def read_acc(self):
        while True:
            acc = self.sense.accel_raw
            print(acc)
            time.sleep(0.1)
            #print(f"x: {acc["x"]}, y: {acc["y"]}, z: {acc["z"]}")

# Case fått data fra accelerometer, men ikke fra GPS
[timestamp, "01", [pos_x, pos_y], [acc_x, acc_y, acc_z]]

# Case fått data fra både accelerometer og GPS
[timestamp, "11", [pos_x, pos_y], [acc_x, acc_y, acc_z]]

if __name__ == "__main__":
    sensor_reader = SensorReader()
    sensor_reader.read_gyro()