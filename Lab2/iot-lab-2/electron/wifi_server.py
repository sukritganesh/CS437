import socket
import picar_4wd as fc
from gpiozero import CPUTemperature
import pickle5 as pickle
import json

HOST = "10.0.0.191" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

def handle_data(data, speed, curr_direction):
    data = data.strip()

    # adjust speed or direction
    if (data == "87"):
        curr_direction = "forward"
        print("going forward ...")
    elif (data == "83"):
        curr_direction = "backward"
        print("backing up ...")
    elif (data == "65"):
        curr_direction = "turn_left"
        print("turning left ...")
    elif (data == "68"):
        curr_direction = "turn_right"
        print("turning right ...")
    elif (data == "32"):
        curr_direction = "standing_still"
        speed = 0
        print("jamming on the brakes")
    elif (data == "54"):
        if (speed <= 95):
            print("speeding up (keanu will really like this)...")
            speed += 5
    elif (data == "52"):
        if (speed >= 5):
            print("slowing down ...")
            speed -= 5

    # actually control the car
    print("to update controls ...")
    if (curr_direction == "forward"):
        fc.forward(speed)
    elif (curr_direction == "backward"):
        fc.backward(speed)
    elif (curr_direction == "turn_left"):
        fc.turn_left(speed)
    elif (curr_direction == "turn_right"):
        fc.turn_right(speed)
    elif (curr_direction == "standing_still"):
        fc.forward(speed)

    print("done with controls")
    return speed, curr_direction

def main():
    speed = 0        # start out with power 10
    curr_direction = "standing_still"   # start out standing still

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        try:
            while 1:
                print("listening to data")
                client, clientInfo = s.accept()
                print("server recv from: ", clientInfo)
                data = client.recv(1024)      # receive 1024 Bytes of message in binary format
                # fc.backward(100)
                if data != b"":
                    # handle data (could either be arrow key, or garbage data sent to ping data read)
                    data_string = data.decode("utf-8", "replace")
                    print("got data:", data_string)
                    speed, curr_direction = handle_data(data_string, speed, curr_direction)

                    # send telemetrics data back to client
                    cpu = CPUTemperature(min_temp=50, max_temp=90)
                    print('temp type:', type(cpu.temperature))
                    return_data = {'echo_data': data_string, 'speed': speed, 'temperature': cpu.temperature, 'direction': curr_direction}
                    print("sending data back")
                    return_data_s = json.dumps(return_data)  
                    client.sendall(bytes(return_data_s, encoding="utf-8")) # Echo back to client
                    # client.sendall(data) # Echo back to client
                print("sent following data back to server:", data)
        except Exception as e: 
            print(e)
            print("Closing socket")
            client.close()
            s.close()    

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()