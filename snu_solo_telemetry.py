###########################################
serial_port='COM7'

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
    subprocess.check_call(["pip", "install", "pyserial"])
    import serial
    
try:
    import customtkinter
except ImportError:
    print('customtkinter is not installed. Installing...')
    subprocess.check_call(["pip", "install", "customtkinter"])
    import customtkinter

###########################################
serial_queue=queue.Queue()

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")





class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # 창 설정
        self.title('SNU Solo Telemetry')
        self.geometry("700x450")
        
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
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        
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
        self.dashboard_frame.grid_columnconfigure(0, weight=1)
        
    ###################################################
    # Raw Data 프레임 설정
    
    def rawdata_frame_init(self):
        self.rawdata_frame = customtkinter.CTkFrame(self,corner_radius=0,fg_color="transparent")
        self.rawdata_frame.grid_columnconfigure(0, weight=1)
        self.rawdata_frame.grid_rowconfigure(6,weight=1)
        self.rawdata_textbox = customtkinter.CTkTextbox(master=self.rawdata_frame, corner_radius=10)
        self.rawdata_textbox.grid(row=5,column=0, sticky='nsew')
        self.rawdata_textbox.insert("0.0", "Some example text!\n" * 50)

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


if __name__ == "__main__":
    app = App()
    app.mainloop()