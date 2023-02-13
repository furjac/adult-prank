import os
import ctypes
import sys
import tkinter as tk
from tkinter import messagebox
import winreg
import subprocess

login = str(os.getlogin())
dire = f'C:/Users/{login}/AppData/Local/vghd'


def is_admin():
    print("Checking root!...")
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def unhide_all_vghd_files(dir):
    print("unhiding and make easy to delete otherwise it will be undeletable.....")
    os.system("attrib -h -s " + dire)
    os.system("attrib -h -s C:/Users/" +
              str(os.getlogin())+"/AppData/Local/Totem")
    for root, dirs, files in os.walk(dir):
        for name in files + dirs:
            file_path = os.path.join(root, name)
            os.system('attrib -h -s "{}"'.format(file_path))


def show_programs_and_feature():
    print("restoring the control panel and system tray....")
    key = winreg.CreateKeyEx(
        winreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
    winreg.DeleteValue(key, "NoTrayItemsDisplay")
    winreg.DeleteKey(key, "DisallowCPL")
    winreg.CloseKey(key)


def delete_startup_script(login):
    print("deleting some important stuffs...")
    file_path = fr'C:\Users\{login}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\script.vbs'
    subprocess.run(['attrib', '-h', '-s', file_path])
    os.remove(file_path)
    startup_key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    winreg.DeleteValue(startup_key, "Virus")
    winreg.CloseKey(startup_key)
    task_mgr = winreg.CreateKeyEx(
        winreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies")
    winreg.DeleteKey(task_mgr, "System")
    winreg.CloseKey(task_mgr)


if __name__ == "__main__":
    if not is_admin():
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Error", "Please run the software as administrator.")
        sys.exit()
    unhide_all_vghd_files(dire)
    show_programs_and_feature()
    delete_startup_script(login=os.getlogin())
