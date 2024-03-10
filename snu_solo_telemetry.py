###########################################
serial_port='COM5'
wheel_radius=0.3 # meter
###########################################
# 필요한 패키지들 불러오기, 없으면 설치

import importlib
import subprocess
import os
import tkinter
import tkinter.messagebox
import threading
import queue


try:
    import serial
except ImportError:
    print('pyserial is not installed. Installing...')
    subprocess.check_call(["python","-m","pip", "install", "pyserial"])
    import serial
    
try:
    import customtkinter
except ImportError:
    print('customtkinter is not installed. Installing...')
    subprocess.check_call(["python","-m","pip", "install", "customtkinter"])
    import customtkinter

###########################################
#serial_data_list="" #queue.Queue()

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

serial_stream = serial.Serial(
    port=serial_port,
    baudrate=115200,
    timeout=1,
)


class App(customtkinter.CTk):
    
    
    
    def __init__(self):
        super().__init__()
        
        # 창 설정
        self.title('SNU Solo Telemetry')
        self.geometry("900x600")
        self.resizable(width=False, height=False)
        
        self.battery_soc=tkinter.StringVar(value='0%')
        self.battery_temp=tkinter.StringVar(value='00℃')
        self.mppt_power=tkinter.StringVar(value='000W')
        self.motor_speed=tkinter.StringVar(value='0.0m/s')
        self.motor_temp=tkinter.StringVar(value='00℃')
        self.motor_power=tkinter.StringVar(value='000W')
        
        self.serial_send_string=tkinter.StringVar(value='')
        read_thread=threading.Thread(target=self.read_from_serial, args=(serial_stream,))
        read_thread.daemon=True
        read_thread.start()
        
        # 왼쪽 프레임 & 오른쪽 화면으로 나누기 설정
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.navigation_frame_init()
        self.dashboard_frame_init()
        self.rawdata_frame_init()
        self.settings_frame_init()
        
        self.select_frame_by_name("dashboard")
        

        
    ###################################################
    # Navigation 프레임 설정
    
    def navigation_frame_init(self):
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="SNU SOLO",
                                                            compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.dashboard_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Dashboard",
                                                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                anchor="w", command=self.dashboard_button_event)
        self.dashboard_button.grid(row=1, column=0, sticky="ew")

        self.rawdata_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Raw Data",
                                                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                anchor="w", command=self.rawdata_button_event)
        self.rawdata_button.grid(row=2, column=0, sticky="ew")

        self.settings_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.settings_button_event)
        self.settings_button.grid(row=3, column=0, sticky="ew")
    
    ###################################################
    # Dashboard 프레임 설정
    
    def dashboard_frame_init(self):
        self.dashboard_frame = customtkinter.CTkFrame(self,corner_radius=0,fg_color="transparent")
        self.dashboard_frame.grid_columnconfigure(0, weight=3)
        self.dashboard_frame.grid_columnconfigure(1, weight=1)
        self.dashboard_frame.grid_rowconfigure(0, weight=1)
        self.dashboard_frame.grid_rowconfigure(1, weight=1)
        self.dashboard_frame.grid_rowconfigure(2, weight=0)
        
        self.battery_frame_init()
        self.solar_frame_init()
        self.motor_frame_init()
        
        
        
        
    def battery_frame_init(self):
        self.battery_frame = customtkinter.CTkFrame(master=self.dashboard_frame, corner_radius=0, fg_color="#1F6AA5")
        self.battery_frame.grid(row=0, column=0, sticky='nsew', padx=(20,10), pady=(20,10))
        
        self.battery_frame.grid_columnconfigure(0, weight=1)
        self.battery_frame.grid_columnconfigure(1, weight=1)
        self.battery_frame.grid_columnconfigure(2, weight=0)
        self.battery_frame.grid_rowconfigure(0, weight=1)
        self.battery_frame.grid_rowconfigure(1, weight=5)
        
        self.battery_frame_title = customtkinter.CTkLabel(master=self.battery_frame,text='Battery', corner_radius=0, font=customtkinter.CTkFont(size=20))
        self.battery_frame_title.grid(row=0, column=0, columnspan=2, pady=(5,0))
        
        self.battery_frame_soc_init()
        self.battery_frame_temp_init()
        
        
    def battery_frame_soc_init(self):
        self.battery_frame_soc = customtkinter.CTkFrame(master=self.battery_frame, corner_radius=0, fg_color="#5994D0")
        self.battery_frame_soc.grid(row=1, column=0, padx=(20,10), pady=(5,20), sticky='nsew')
        
        self.battery_frame_soc.grid_columnconfigure(0, weight=1)
        self.battery_frame_soc.grid_rowconfigure(0, weight=1)
        
        self.battery_frame_soc_text = customtkinter.CTkLabel(master=self.battery_frame_soc, textvariable=self.battery_soc, font=customtkinter.CTkFont(size=50))
        self.battery_frame_soc_text.grid(row=0, column=0)
        
    def battery_frame_temp_init(self):
        self.battery_frame_temp = customtkinter.CTkFrame(master=self.battery_frame, corner_radius=0, fg_color="#5994D0")
        self.battery_frame_temp.grid(row=1, column=1, padx=(10,20), pady=(5,20), sticky='nsew')
        
        self.battery_frame_temp.grid_columnconfigure(0, weight=1)
        self.battery_frame_temp.grid_rowconfigure(0, weight=1)
        
        self.battery_frame_temp_text = customtkinter.CTkLabel(master=self.battery_frame_temp, textvariable=self.battery_temp, font=customtkinter.CTkFont(size=50))
        self.battery_frame_temp_text.grid(row=0, column=0)
        
        
        
        
    def solar_frame_init(self):
        self.solar_frame = customtkinter.CTkFrame(master=self.dashboard_frame, corner_radius=0, fg_color="#D54B28")
        self.solar_frame.grid(row=0, column=1, sticky='nsew', padx=(10,20), pady=(20,10))
        
        self.solar_frame.grid_columnconfigure(0, weight=1)
        self.solar_frame.grid_columnconfigure(1, weight=0)
        self.solar_frame.grid_rowconfigure(0, weight=1)
        self.solar_frame.grid_rowconfigure(1, weight=5)
        
        self.solar_frame_title = customtkinter.CTkLabel(master=self.solar_frame,text='Solar', corner_radius=0, font=customtkinter.CTkFont(size=20))
        self.solar_frame_title.grid(row=0, column=0, pady=(5,0))
    
        self.solar_frame_mppt_init()
        
    
    def solar_frame_mppt_init(self):        
        self.solar_frame_mppt = customtkinter.CTkFrame(master=self.solar_frame, corner_radius=0, fg_color="#F57B58")
        self.solar_frame_mppt.grid(row=1, column=0, padx=(20,20), pady=(5,20), sticky='nsew')
        
        self.solar_frame_mppt.grid_columnconfigure(0, weight=1)
        self.solar_frame_mppt.grid_rowconfigure(0, weight=1)
        
        self.solar_frame_mppt_text = customtkinter.CTkLabel(master=self.solar_frame_mppt, textvariable=self.mppt_power, font=customtkinter.CTkFont(size=50))
        self.solar_frame_mppt_text.grid(row=0,column=0)
        
        
        
        
    def motor_frame_init(self):
        self.motor_frame = customtkinter.CTkFrame(master=self.dashboard_frame, corner_radius=0, fg_color="#5234AC")
        self.motor_frame.grid(row=1, column=0, sticky='nsew', padx=(20,20), pady=(10,20), columnspan=2)
        
        self.motor_frame.grid_columnconfigure(0, weight=1)
        self.motor_frame.grid_columnconfigure(1, weight=1)
        self.motor_frame.grid_columnconfigure(2, weight=1)
        self.motor_frame.grid_columnconfigure(3, weight=0)
        self.motor_frame.grid_rowconfigure(0, weight=1)
        self.motor_frame.grid_rowconfigure(1, weight=5)
        
        self.motor_frame_title = customtkinter.CTkLabel(master=self.motor_frame,text='Motor', corner_radius=0, font=customtkinter.CTkFont(size=20))
        self.motor_frame_title.grid(row=0, column=0, columnspan=3, pady=(5,0))
        
        self.motor_frame_speed_init()
        self.motor_frame_temp_init()
        self.motor_frame_watt_init()
        
        
    def motor_frame_speed_init(self):
        self.motor_frame_speed = customtkinter.CTkFrame(master=self.motor_frame, corner_radius=0, fg_color="#9F87C2")
        self.motor_frame_speed.grid(row=1, column=0, padx=(20,10), pady=(5,20), sticky='nsew')
        
        self.motor_frame_speed.grid_columnconfigure(0, weight=1)
        self.motor_frame_speed.grid_rowconfigure(0, weight=1)        
        
        self.motor_frame_speed_text = customtkinter.CTkLabel(master=self.motor_frame_speed, textvariable=self.motor_speed, font=customtkinter.CTkFont(size=50))
        self.motor_frame_speed_text.grid(row=0,column=0)
        
        
    def motor_frame_temp_init(self):
        self.motor_frame_temp = customtkinter.CTkFrame(master=self.motor_frame, corner_radius=0, fg_color="#9F87C2")
        self.motor_frame_temp.grid(row=1, column=1, padx=(10,10), pady=(5,20), sticky='nsew')
        
        self.motor_frame_temp.grid_columnconfigure(0, weight=1)
        self.motor_frame_temp.grid_rowconfigure(0, weight=1)        
        
        self.motor_frame_temp_text = customtkinter.CTkLabel(master=self.motor_frame_temp, textvariable=self.motor_temp, font=customtkinter.CTkFont(size=50))
        self.motor_frame_temp_text.grid(row=0,column=0)       
    
    
    def motor_frame_watt_init(self):
        self.motor_frame_watt = customtkinter.CTkFrame(master=self.motor_frame, corner_radius=0, fg_color="#9F87C2")
        self.motor_frame_watt.grid(row=1, column=2, padx=(10,20), pady=(5,20), sticky='nsew')
        
        self.motor_frame_watt.grid_columnconfigure(0, weight=1)
        self.motor_frame_watt.grid_rowconfigure(0, weight=1)        
        
        self.motor_frame_watt_text = customtkinter.CTkLabel(master=self.motor_frame_watt, textvariable=self.motor_power, font=customtkinter.CTkFont(size=50))
        self.motor_frame_watt_text.grid(row=0,column=0)
        
        
        
    ###################################################
    # Raw Data 프레임 설정
    
    def rawdata_frame_init(self):
        self.rawdata_frame = customtkinter.CTkFrame(self,corner_radius=0,fg_color="transparent")
        
        self.rawdata_frame.grid_columnconfigure(0, weight=15)
        self.rawdata_frame.grid_columnconfigure(1, weight=1)
        self.rawdata_frame.grid_rowconfigure(0,weight=15)
        self.rawdata_frame.grid_rowconfigure(1,weight=1)
        
        self.rawdata_textbox = customtkinter.CTkTextbox(master=self.rawdata_frame, corner_radius=0, wrap='none')
        self.rawdata_textbox.grid(row=0,column=0, sticky='nsew', columnspan=2)
        
        self.rawdata_entry = customtkinter.CTkEntry(master=self.rawdata_frame, textvariable=self.serial_send_string, corner_radius=0)
        self.rawdata_entry.grid(row=1,column=0, sticky='nsew')
        
        self.rawdata_send_button = customtkinter.CTkButton(master=self.rawdata_frame, text='Send', corner_radius=0, command=self.rawdata_send_button_event)
        self.rawdata_send_button.grid(row=1, column=1, sticky='nsew')
        #self.rawdata_textbox.insert("0.0", "Some example text!\n" * 50)

    ###################################################
    # Settings 프레임 설정
    
    def settings_frame_init(self):
        self.settings_frame = customtkinter.CTkFrame(self,corner_radius=0,fg_color="transparent")
        self.settings_frame.grid_columnconfigure(0, weight=1)

    ###################################################
    # Button 동작 설정
    def dashboard_button_event(self):
        self.select_frame_by_name("dashboard")
    def rawdata_button_event(self):
        self.select_frame_by_name("rawdata")
    def settings_button_event(self):
        self.select_frame_by_name("settings")
    
    def rawdata_send_button_event(self):
        user_input=self.serial_send_string.get()+'\r\n'
        self.serial_send_string.set('')
        serial_stream.write(user_input.encode())
        self.rawdata_textbox.insert(index=tkinter.END,text=user_input)
        
    
    ###################################################
    # Frame 설정
    def select_frame_by_name(self, name):
        self.dashboard_button.configure(fg_color=("gray75", "gray25") if name == "dashboard" else "transparent")
        self.rawdata_button.configure(fg_color=("gray75", "gray25") if name == "rawdata" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")

        if name == "dashboard":
            self.dashboard_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.dashboard_frame.grid_forget()
            
        if name == "rawdata":
            self.rawdata_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.rawdata_frame.grid_forget()
            
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()


    
    ###################################################
    # Serial Read 설정
    def read_from_serial(self, serial_stream):
        while True:
            data=serial_stream.readline().decode().strip()
            if data:
                print(f'{data}')
                self.rawdata_textbox.insert(index=tkinter.END,text=data+'\n')
                self.rawdata_textbox.see(tkinter.END)
                
            if data.startswith("+RCV="):
                received_data=data[len("+RCV="):]
                payload_data=received_data.split(',')[2]
                
                if (len(payload_data.split('/'))==6):
                    (battery_SOC, battery_TEMP, mppt_POWER, motor_SPEED, motor_TEMP, motor_POWER) = payload_data.split('/')
                    self.battery_soc.set(self.check_numeric(battery_SOC)+'%')
                    self.battery_temp.set(self.check_numeric(battery_TEMP)+'℃')
                    self.mppt_power.set(self.check_numeric(mppt_POWER)+'W')
                    self.motor_temp.set(self.check_numeric(motor_TEMP)+'℃')
                    self.motor_power.set(self.check_numeric(motor_POWER)+'W')
                    speed=self.check_numeric(motor_SPEED)
                    if(speed=='Err '):
                        self.motor_speed.set('Err m/s')
                    else:
                        self.motor_speed.set(str(round(float(speed)/60*wheel_radius,1))+'m/s')
    
    
    def check_numeric(self, value):
        try:
            numeric_value = round(float(value),1)
            return str(numeric_value)
        except ValueError:
            return 'Err '
    ###################################################





if __name__ == "__main__":
    app = App()
    app.mainloop()