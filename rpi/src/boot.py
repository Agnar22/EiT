
from sense_hat import SenseHat
import subprocess
import sys
import os
import requests

os.chdir(os.path.dirname(os.path.abspath(__file__)))

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
off = (0, 0, 0)

sensor_status = off
sync_status = off
server_connection_status = off

ping_url = "http://212.251.162.131:2326/ping"
bearer_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvaG4iLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjE2MTQ3NjE0MDZ9.sJ4huAOIHHEQm2LqRZYiFADeluhB10XkBiJosOLJp6A'

def set_sensor_status(color):
    global sensor_status
    sensor_status = color

def set_sync_status(color):
    global sync_status
    sync_status = color

def set_server_connection_status(color):
    global server_connection_status
    server_connection_status = color

def set_status_lights():
    sense.clear()
    sense.set_pixel(0, 0, server_connection_status)
    sense.set_pixel(1, 0, sync_status)
    sense.set_pixel(2, 0, sensor_status)

def start_sensors(debug=False):

    if debug:
        sense.show_message("start sensor")
    
    set_sensor_status(blue)
    
    try:
        subprocess.run(["sudo python3 ./logging/sensors.py &"], check=True, shell=True)
    except Exception as e:
        print("Failed to start sensor logging script")
        print(e)
        set_logging_status(red)
        return False

    if debug:
        sense.show_message("ok")

    set_sensor_status(green)
    
    return True


def start_synching(debug=False):

    if debug:
        sense.show_message("start sync")

    set_sync_status(blue)

    try:
        subprocess.run(["sudo python3 ./sync/sync.py &"], check=True, shell=True)
    except Exception as e:
        print("Failed to start data synching")
        print(e)
        set_sync_status(red)
        return False

    if debug:
        sense.show_message("ok")

    set_sync_status(green)
    
    return True

def check_server_connection(retry_count=10, debug=False):
    
    if debug:
        sense.show_message("ping")

    set_server_connection_status(blue)
    
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
    
    if success:
        print(f"Successfully pinged server. Status_code: {status_code} Content: {content}")
        if debug:
            sense.show_message("ok")
        set_server_connection_status(green)
        return True
    else:
        print("Failed to ping server")
        set_server_connection_status(red)
        return False

def main():
    debug = False
    sense.show_message("verbose y > n <")
    event = sense.stick.wait_for_event()
    if event.direction == "right":
        debug = True

    # Check server connection
    start_offline = False
    while not start_offline:
        if check_server_connection(debug=debug) == False:
            sense.show_message("cont. w/o inet > or retry < ?")
            event = sense.stick.wait_for_event()
            if event.direction == "left":
                continue
            else:
                start_offline = True
                set_sync_status(yellow)
        
        else:
            # Start synching
            start_synching(debug=debug)
            break

    # Start sensors
    sensor_success = False
    while not sensor_success:
        sensor_success = start_sensors(debug=debug)

        if not sensor_success:
            sense.show_message("fail retry < exit >")
            
            event = sense.stick.wait_for_event()
            if event.direction == "right":
                sense.show_message("exiting")
                sys.exit()
            else:
                continue
        else:
            break

    sense.show_message("starting")
    set_status_lights()


if __name__ == "__main__":
    sense = SenseHat()
    sense.clear()
    main()

