import subprocess
import os
import tkinter as tk
from tkinter import messagebox

def list_remote_files(target_code):
    rclone_exe = os.path.join(os.path.dirname(__file__), 'rclone.exe')
    rclone_conf = os.path.join(os.path.dirname(__file__), 'rclone.conf')
    remote_path = f"personal:/311/{target_code}/"

    if not os.path.isfile(rclone_exe):
        raise FileNotFoundError("未找到rclone.exe")
    if not os.path.isfile(rclone_conf):
        raise FileNotFoundError("未找到rclone.conf")

    try:
        result = subprocess.run([rclone_exe, '--config', rclone_conf, 'lsf', remote_path], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip().split('\n')
        else:
            raise RuntimeError(f"列出远程文件时出错：{result.stderr}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"列出远程文件时出错：{e}")

def download_from_rclone(file_path, target_code, show_messagebox=True):
    rclone_exe = os.path.join(os.path.dirname(__file__), 'rclone.exe')
    rclone_conf = os.path.join(os.path.dirname(__file__), 'rclone.conf')
    remote_path = f"personal:/311/{target_code}/" + os.path.basename(file_path)

    if not os.path.isfile(rclone_exe):
        raise FileNotFoundError("未找到rclone.exe")
    if not os.path.isfile(rclone_conf):
        raise FileNotFoundError("未找到rclone.conf")

    try:
        # 调用rclone命令下载文件并覆盖本地文件
        subprocess.run([rclone_exe, '--config', rclone_conf, 'copy', remote_path, os.path.dirname(file_path)], check=True)
        if show_messagebox:
            messagebox.showinfo("下载成功", "文件下载并覆盖成功！")
    except subprocess.CalledProcessError as e:
        if "not found" in str(e.stderr):
            raise FileNotFoundError(f"未找到文件：{os.path.basename(file_path)}")
        else:
            raise RuntimeError(f"下载文件时出错：{e}")

def download_from_rclone_with_selection(file_path, selected_file, target_code, show_messagebox=True):
    rclone_exe = os.path.join(os.path.dirname(__file__), 'rclone.exe')
    rclone_conf = os.path.join(os.path.dirname(__file__), 'rclone.conf')
    remote_path = f"personal:/311/{target_code}/" + selected_file

    if not os.path.isfile(rclone_exe):
        raise FileNotFoundError("未找到rclone.exe")
    if not os.path.isfile(rclone_conf):
        raise FileNotFoundError("未找到rclone.conf")

    try:
        # 调用rclone命令下载文件并覆盖本地文件
        subprocess.run([rclone_exe, '--config', rclone_conf, 'copy', remote_path, os.path.dirname(file_path)], check=True)
        if show_messagebox:
            messagebox.showinfo("下载成功", "文件下载并覆盖成功！")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"下载文件时出错：{e}")
