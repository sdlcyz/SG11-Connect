import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import random
import string
import keyboard
import threading
from plyer import notification
import winsound
import ctypes
import upload
import download

# 创建主窗口
root = tk.Tk()
root.title("三国志11存档快速传输工具")
root.geometry("600x300")
root.configure(bg="#f0f0f0")

# 设置图标
icon = Image.open("icon.png")  # 请替换为实际的图标文件路径
photo = ImageTk.PhotoImage(icon)
root.iconphoto(False, photo)

# 应用现代主题
style = ttk.Style()
style.theme_use("clam")

# 检查操作系统版本
def is_windows_7():
    return ctypes.windll.kernel32.GetVersion() & 0x80000000

# 播放提示音
def play_sound():
    winsound.MessageBeep()

# 发送通知
def send_notification(title, message):
    try:
        notification.notify(
            title=title,
            message=message,
            app_name='三国志11存档快速传输工具',
            timeout=10
        )
    except:
        pass

# 上传操作
def upload_operation():
    send_notification("上传操作", "上传操作已开始")
    play_sound()
    try:
        file_path = file_entry.get()
        target_code = code_entry.get()
        if file_path and target_code:
            upload.upload_to_rclone(file_path, target_code, show_messagebox=False)
        send_notification("上传操作", "上传操作已完成")
        play_sound()
    except Exception as e:
        send_notification("上传操作", f"上传操作失败：{e}")
        play_sound()

# 下载操作
def download_operation():
    send_notification("下载操作", "下载操作已开始")
    play_sound()
    try:
        file_path = file_entry.get()
        target_code = code_entry.get()
        if file_path and target_code:
            download.download_from_rclone(file_path, target_code, show_messagebox=False)
        send_notification("下载操作", "下载操作已完成")
        play_sound()
    except Exception as e:
        send_notification("下载操作", f"下载操作失败：{e}")
        play_sound()

# 监听键盘事件
def listen_keyboard():
    keyboard.add_hotkey('shift+F1', upload_operation)
    keyboard.add_hotkey('shift+F2', download_operation)
    keyboard.wait()

# 文件选择功能
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("所有文件", "*.*")])
    if file_path:
        # 在输入框中显示文件路径
        file_entry.delete(0, tk.END)  # 清空输入框
        file_entry.insert(0, file_path)  # 插入文件路径
        messagebox.showinfo("文件路径", f"你选择的文件是：{file_path}")
    else:
        messagebox.showwarning("未选择文件", "你没有选择任何文件。")

# 上传文件功能
def upload_file():
    file_path = file_entry.get()
    target_code = code_entry.get()
    if file_path and target_code:
        try:
            upload.upload_to_rclone(file_path, target_code)
        except Exception as e:
            messagebox.showerror("上传失败", f"文件上传失败：{e}")
    else:
        messagebox.showwarning("信息不完整", "请选择文件并输入对方连接码。")

# 下载文件功能
def download_file():
    file_path = file_entry.get()
    target_code = code_entry.get()
    if file_path and target_code:
        try:
            download.download_from_rclone(file_path, target_code)
        except FileNotFoundError as e:
            remote_files = download.list_remote_files(target_code)
            if remote_files:
                selected_file = filedialog.askstring("选择文件", "请选择要下载的文件：", initialvalue=remote_files[0])
                if selected_file and selected_file in remote_files:
                    download.download_from_rclone_with_selection(file_path, selected_file, target_code)
                else:
                    messagebox.showinfo("取消下载", "你取消了下载。")
            else:
                messagebox.showerror("下载失败", "远程目录中没有文件。")
        except Exception as e:
            messagebox.showerror("下载失败", f"文件下载失败：{e}")
    else:
        messagebox.showwarning("信息不完整", "请选择文件并输入对方连接码。")

# 生成随机连接码
def generate_connection_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# 创建主窗口时生成连接码
connection_code = generate_connection_code()

# 显示连接码的标签
code_label = tk.Label(root, text=f"您的连接码: {connection_code}")
code_label.pack(pady=5)

# 创建输入连接码的输入框
code_entry = tk.Entry(root, width=20)
code_entry.pack(pady=5)
code_entry.insert(0, "输入对方连接码")

# 创建文件选择按钮
select_button = tk.Button(root, text="选择文件", command=select_file)
select_button.pack(pady=10)

# 创建输入框
file_entry = tk.Entry(root, width=50)
file_entry.pack(pady=10)

# 创建一个框架来包含上传和下载按钮
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# 创建上传按钮
upload_button = tk.Button(button_frame, text="上传", command=upload_file)
upload_button.grid(row=0, column=0, padx=5)

# 创建下载按钮
download_button = tk.Button(button_frame, text="下载", command=download_file)
download_button.grid(row=0, column=1, padx=5)

# 启动监听键盘事件的线程
keyboard_thread = threading.Thread(target=listen_keyboard)
keyboard_thread.daemon = True
keyboard_thread.start()

# 启动主事件循环
root.mainloop()
