import json
import requests
import os
import time
from csv import reader
from typing import List

os.chdir(os.path.dirname(os.path.abspath(__file__)))

url = 'http://212.251.162.131:2326/datapoints_all_sensors'
data_dir = '../../data/current_log/'
sleep_time = 4
bearer_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvaG4iLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjE2MTQ3NjE0MDZ9.sJ4huAOIHHEQm2LqRZYiFADeluhB10XkBiJosOLJp6A'


def read_csv(file_name: str) -> List[List[float]]:
  with open(file_name, 'r+') as f:
    rows = list(reader(f))
    conv_rows = []
    for row in rows:
        curr_row = []
        for element in row:
            if element == 'None' or element is None or element == '':
                curr_row.append(None)
            else:
                try:
                    curr_row.append("{:.2f}".format(float(element)))
                except ValueError:
                    curr_row.append(element)
        conv_rows.append(curr_row)
    return conv_rows


def post_data(data: List[List[float]])->int:
  # print(data)
  # print(json.dumps(data))
  return requests.post(url,
    headers={
      "Authorization": "Bearer "+bearer_token
    },
    json={
      "values": data
  }).status_code


def sync_data_loop():
  while True:
    for file in os.listdir(data_dir):
      data = read_csv(data_dir+file)
      try:
          status_code = post_data(data)
      except requests.exceptions.ConnectionError:
          print("No connection to server")
          continue
      print(f'status_code {status_code}')
      if status_code == 201:
        os.remove(data_dir+file)
    time.sleep(sleep_time)

if __name__ == '__main__':
  sync_data_loop()
