import serial
import threading
import random
import time


ser = serial.Serial(
    port='COM7',
    baudrate=115200,
    timeout=0)


address = 0


def read_from_port(ser):
    while True:
        # 시리얼 포트에서 데이터 읽기
        data = ser.readline().decode().strip()
        if data:
            print(f'{data}')



# 키보드 입력을 받아 시리얼 포트로 전송하는 함수
def write_to_port(ser):
    while True:
        # 사용자로부터 키보드 입력 받기
        #user_input = input('\n')
        #user_input+='\r\n'
        # 시리얼 포트로 데이터 전송
        #ser.write(user_input.encode())
        
        battery_soc = random_float(0.0, 100.0)
        battery_temp = random_float(-40.0, 100.0)
        mppt_power = random_float(0.0, 1000.0)
        motor_rpm = random_float(-150.0, 150.0)
        motor_temp = random_float(-40.0, 100.0)
        motor_power = random_float(-100.0, 1000.0)
        
        sensor_data = battery_soc+"/"+battery_temp+"/"+mppt_power+"/"+motor_rpm+"/"+motor_temp+"/"+motor_power
        length = len(sensor_data)
        
        send_data = "AT+SEND="+str(address)+","+str(length)+","+sensor_data+"\r\n"
        ser.write(send_data.encode())
        print(send_data)
        
        time.sleep(1)
        
        
        
        
        
        
        
        

def random_float(start, end):
    a = random.uniform(start, end)
    b = round(a,1)
    c = str(b)
    return c



# 시리얼 포트에서 데이터를 읽고 출력하는 스레드 시작
read_thread = threading.Thread(target=read_from_port, args=(ser,))
read_thread.daemon = True
read_thread.start()

# 키보드 입력을 받아 시리얼 포트로 전송하는 스레드 시작
write_thread = threading.Thread(target=write_to_port, args=(ser,))
write_thread.daemon = True
write_thread.start()

# 메인 스레드 유지
while True:
    pass
