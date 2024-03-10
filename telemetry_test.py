import serial
import threading


ser = serial.Serial(
    port='COM7',
    baudrate=115200,
    timeout=0)



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
        user_input = input('\n')
        user_input+='\r\n'
        # 시리얼 포트로 데이터 전송
        ser.write(user_input.encode())



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
