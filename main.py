import pyautogui
import tkinter as tk
import clipboard
import keyboard
from PIL import Image, ImageTk, ImageGrab, ImageDraw

coordinates_list = []
format_text = "{x}, {y}, {rgb}"  # 用来保存输入框中的格式
color_format = "rgb"  # 用来保存选择的颜色格式，默认为 "rgb"

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

    if color_format == "rgb":
        rgb_text.config(state=tk.NORMAL)
        rgb_text.delete("1.0", tk.END)
        rgb_text.insert(tk.END, f"RGB: {rgb_color}\n")
        rgb_text.config(state=tk.DISABLED)
    elif color_format == "hex":
        hex_color = "#{:02x}{:02x}{:02x}".format(*rgb_color)
        rgb_text.config(state=tk.NORMAL)
        rgb_text.delete("1.0", tk.END)
        rgb_text.insert(tk.END, f"HEX: {hex_color}\n")
        rgb_text.config(state=tk.DISABLED)

    clipboard_text = format_text.format(x=x, y=y, rgb=rgb_color)
    clipboard.copy(clipboard_text)

def update_coordinates_text():
    coordinates_text.config(state=tk.NORMAL)
    coordinates_text.delete("1.0", tk.END)
    for coordinate in coordinates_list:
        x, y, rgb_color = coordinate
        if color_format == "rgb":
            formatted_text = format_text.format(x=x, y=y, rgb=rgb_color)
        elif color_format == "hex":
            hex_color = "#{:02x}{:02x}{:02x}".format(*rgb_color)
            formatted_text = format_text.replace("{x}", str(x)).replace("{y}", str(y)).replace("{rgb}", hex_color)
        coordinates_text.insert(tk.END, formatted_text + "\n")
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
    screenshot = ImageGrab.grab(bbox=(x-50, y-50, x+50, y+50))  # 将区域缩小到1/4
    # 缩放截图
    magnified_screenshot = screenshot.resize((200, 200), Image.LANCZOS)  # 缩小预览区域为原来的1/4

    # 在截图上绘制鼠标光标
    draw = ImageDraw.Draw(magnified_screenshot)
    draw.rectangle([(97, 97), (103, 103)], outline="red")  # 缩小预览区域后，光标位置也需要缩小1/4

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

def on_color_format_change():
    global color_format
    color_format = color_var.get()
    update_coordinates_text()

def on_format_entry_change(event):
    global format_text
    format_text = format_entry.get()
    update_coordinates_text()

def set_default_format(event):
    global format_text
    if format_entry.get() == "":
        format_entry.insert(0, format_text)

def apply_format():
    global format_text
    format_text = format_entry.get()
    update_coordinates_text()

root = tk.Tk()
root.title("Mouse and RGB Tracker@雪导")

# 设置窗口大小
window_width = 350
window_height = 520
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

# 添加颜色格式单选选项框
color_var = tk.StringVar(value="rgb")
color_format_frame = tk.Frame(root)
color_format_frame.pack()

rgb_radio = tk.Radiobutton(color_format_frame, text="RGB", variable=color_var, value="rgb", command=on_color_format_change)
rgb_radio.pack(side=tk.LEFT)

hex_radio = tk.Radiobutton(color_format_frame, text="十六进制", variable=color_var, value="hex", command=on_color_format_change)
hex_radio.pack(side=tk.LEFT)

# 添加输入框和确认按钮
format_frame = tk.Frame(root)  # 新建一个框架用于放置格式相关的控件
format_frame.pack(pady=5)

format_label = tk.Label(format_frame, text="复制格式：")
format_label.grid(row=0, column=0)

format_entry = tk.Entry(format_frame, width=30)
format_entry.insert(tk.END, format_text)
format_entry.grid(row=0, column=1)

apply_button = tk.Button(format_frame, text="确认", command=apply_format)
apply_button.grid(row=0, column=2)

# 当输入框获得焦点时，显示默认格式
format_entry.bind("<FocusIn>", set_default_format)

# 添加说明标签
instructions_label = tk.Label(root, text="说明：使用 Shift+Enter 进行抓捕")
instructions_label.pack()

# 放大镜
magnifier_label = tk.Label(root)
magnifier_label.pack()

# 绑定输入框内容改变事件
format_entry.bind("<FocusOut>", on_format_entry_change)

# 创建复选框和标签所在的Frame，并使用grid布局管理器
checkbox_and_label_frame = tk.Frame(root)
checkbox_and_label_frame.pack()

stay_on_top_var = tk.IntVar()
stay_on_top_checkbox = tk.Checkbutton(checkbox_and_label_frame, text="Stay on Top", variable=stay_on_top_var, command=toggle_stay_on_top)
stay_on_top_checkbox.grid(row=0, column=0)

# 绑定按键事件
keyboard.add_hotkey("shift+enter", on_shift_enter)

# 启动放大镜更新
update_magnifier()

root.mainloop()
