import requests
import os
import time
from csv import reader
from typing import List

url = 'http://agnar.sanderkk.com:2326/datapoints'
data_dir = '../data/data_to_sync/'
sleep_time = 0.3
bearer_token = ''


def read_csv(file_name: str) -> List[List[float]]:
  with open(file_name, 'r+') as f:
    rows = list(reader(f))
    rows = list(map(lambda row: list(map(float, row)), rows))
    return rows


def post_data(data: List[List[float]])->int:
  print(data)
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
      status_code = post_data(data)
      if status_code == 201:
        os.remove(data_dir+file)
    time.sleep(sleep_time)

if __name__ == '__main__':
  sync_data_loop()
