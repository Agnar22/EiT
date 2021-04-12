import requests
from sense_hat import SenseHat
import time

ping_url = "http://212.251.162.131:2326/ping"
bearer_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvaG4iLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjE2MTQ3NjE0MDZ9.sJ4huAOIHHEQm2LqRZYiFADeluhB10XkBiJosOLJp6A'


def check_server_connection(retry_count=10):
    
    success = False

    for i in range(retry_count):
        try:
            response = requests.get(
                    ping_url,
                    headers={"Authorization": "Bearer " + bearer_token}
                    )
            status_code = response.status_code
            content = response.content
            if status_code == 200 and response.content == b'pong':
                success = True
                break

        except Exception as e:
            print("No answer from server")
            print(e)
            continue
    
    return success

def main(freq=0.25):
    
    sense = SenseHat()

    while True:
        if check_server_connection():
            # Toggle green LED
            val = sense.get_pixel(0,0)
            if val == [0, 0, 0]:
                sense.set_pixel(0, 0, (0, 255, 0))
            else:
                sense.set_pixel(0, 0, (0, 0, 0))
        else:
            sense.set_pixel(0, 0, (255, 0, 0))

        time.sleep(1/freq)


if __name__ == "__main__":
    main()

