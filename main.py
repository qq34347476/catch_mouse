import pyautogui
import tkinter as tk
import clipboard
import keyboard
from PIL import Image, ImageTk, ImageGrab, ImageDraw

coordinates_list = []
format_text = ""  # 用来保存输入框中的格式

def get_mouse_position_and_rgb():
    x, y = pyautogui.position()
    rgb_color = pyautogui.screenshot().getpixel((x, y))

    x_text.config(state=tk.NORMAL)
    x_text.delete("1.0", tk.END)
    x_text.insert(tk.END, f"X: {x}\n")
    x_text.config(state=tk.DISABLED)

    y_text.config(state=tk.NORMAL)
    y_text.delete("1.0", tk.END)
    y_text.insert(tk.END, f"Y: {y}\n")
    y_text.config(state=tk.DISABLED)

    rgb_text.config(state=tk.NORMAL)
    rgb_text.delete("1.0", tk.END)
    rgb_text.insert(tk.END, f"RGB: {rgb_color}\n")
    rgb_text.config(state=tk.DISABLED)

    clipboard.copy(f"X: {x}, Y: {y}, RGB: {rgb_color}")

def update_coordinates_text():
    coordinates_text.config(state=tk.NORMAL)
    coordinates_text.delete("1.0", tk.END)
    for coordinate in coordinates_list:
        x, y, rgb_color = coordinate
        coordinates_text.insert(tk.END, f"X: {x}, Y: {y}, RGB: {rgb_color}\n")
    coordinates_text.config(state=tk.DISABLED)

def on_shift_enter():
    get_mouse_position_and_rgb()
    # 添加坐标信息到列表中
    coordinates_list.append(pyautogui.position() + (pyautogui.screenshot().getpixel(pyautogui.position()),))

    # 如果列表长度超过十个，则删除最旧的坐标信息
    if len(coordinates_list) > 10:
        coordinates_list.pop(0)

    # 更新显示坐标信息的文本框
    update_coordinates_text()

def update_magnifier():
    x, y = pyautogui.position()
    # 获取屏幕区域的截图，并将截图的大小调整为更大的值
    screenshot = ImageGrab.grab(bbox=(x-100, y-100, x+100, y+100))
    # 缩放截图
    magnified_screenshot = screenshot.resize((400, 400), Image.LANCZOS)

    # 在截图上绘制鼠标光标
    draw = ImageDraw.Draw(magnified_screenshot)
    draw.rectangle([(195, 195), (205, 205)], outline="red")

    # 转换为Tkinter PhotoImage
    magnified_photo = ImageTk.PhotoImage(magnified_screenshot)
    magnifier_label.config(image=magnified_photo)
    magnifier_label.image = magnified_photo

    # 在0.2秒后再次更新放大镜内容
    root.after(200, update_magnifier)

def toggle_stay_on_top():
    if stay_on_top_var.get() == 1:
        root.wm_attributes("-topmost", True)
    else:
        root.wm_attributes("-topmost", False)

root = tk.Tk()
root.title("Mouse and RGB Tracker   @雪导")

# 设置窗口大小
window_width = 400
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width - window_width) / 2)
y_coordinate = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

x_text = tk.Text(root, height=1, width=20, wrap=tk.NONE, state=tk.DISABLED)
x_text.pack()

y_text = tk.Text(root, height=1, width=20, wrap=tk.NONE, state=tk.DISABLED)
y_text.pack()

rgb_text = tk.Text(root, height=1, width=20, wrap=tk.NONE, state=tk.DISABLED)
rgb_text.pack()

coordinates_text = tk.Text(root, height=10, width=40, wrap=tk.NONE, state=tk.DISABLED)
coordinates_text.pack()


# 创建复选框和标签所在的Frame，并使用grid布局管理器
checkbox_and_label_frame = tk.Frame(root)
checkbox_and_label_frame.pack()

stay_on_top_var = tk.IntVar()
stay_on_top_checkbox = tk.Checkbutton(checkbox_and_label_frame, text="Stay on Top", variable=stay_on_top_var, command=toggle_stay_on_top)
stay_on_top_checkbox.grid(row=0, column=0)

# 添加文字说明标签
shift_enter_label = tk.Label(checkbox_and_label_frame, text="按住Shift+Enter进行截图")
shift_enter_label.grid(row=0, column=1)

# 放大镜
magnifier_label = tk.Label(root)
magnifier_label.pack()

# 绑定按键事件
keyboard.add_hotkey("shift+enter", on_shift_enter)

# 启动放大镜更新
update_magnifier()

root.mainloop()
