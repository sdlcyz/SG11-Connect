import subprocess
import os
import tkinter as tk
from tkinter import messagebox

def get_remote_file_size(file_path, remote_path, rclone_exe, rclone_conf):
    result = subprocess.run([rclone_exe, '--config', rclone_conf, 'lsf', '--format', 's', remote_path + os.path.basename(file_path)],
                            capture_output=True, text=True)
    if result.returncode == 0 and result.stdout.strip():
        return int(result.stdout.strip())
    return None

def upload_to_rclone(file_path, target_code, show_messagebox=True):
    rclone_exe = os.path.join(os.path.dirname(__file__), 'rclone.exe')
    rclone_conf = os.path.join(os.path.dirname(__file__), 'rclone.conf')
    remote_path = f"personal:/311/{target_code}/"

    if not os.path.isfile(rclone_exe):
        raise FileNotFoundError("未找到rclone.exe")
    if not os.path.isfile(rclone_conf):
        raise FileNotFoundError("未找到rclone.conf")

    try:
        local_file_size = os.path.getsize(file_path)
        remote_file_size = get_remote_file_size(file_path, remote_path, rclone_exe, rclone_conf)

        if remote_file_size is not None and local_file_size == remote_file_size:
            if show_messagebox:
                root = tk.Tk()
                root.withdraw()
                if not messagebox.askyesno("文件已存在", f"{file_path}已存在且大小相同，是否仍然上传？"):
                    return

        # 调用rclone命令上传文件
        subprocess.run([rclone_exe, '--config', rclone_conf, 'copy', file_path, remote_path], check=True)
        if show_messagebox:
            messagebox.showinfo("上传成功", "文件上传成功！")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"上传文件时出错：{e}")
