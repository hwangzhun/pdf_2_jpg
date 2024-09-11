import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
from pdf_to_images import pdf_to_images
from file_operations import copy_pdf_to_output
import sys

def select_input_files():
    input_files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if input_files:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, ";".join(input_files))

def select_output_dir():
    output_dir = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_dir)

def process_pdfs():
    input_files = input_entry.get().split(";")
    output_dir = output_entry.get()

    if not input_files or not output_dir:
        messagebox.showerror("错误", "请选择输入文件和输出目录")
        return

    # 设置 Poppler 路径为相对路径
    if getattr(sys, 'frozen', False):  # 如果被打包成了 EXE
        poppler_path = os.path.join(sys._MEIPASS, 'poppler', 'bin')
    else:  # 未打包时（开发模式下）
        poppler_path = os.path.join(os.getcwd(), 'poppler', 'bin')

    total_files = len(input_files)
    progress['maximum'] = total_files

    for idx, pdf_path in enumerate(input_files):
        try:
            # 更新进度条和当前处理状态
            progress['value'] = idx + 1
            status_label.config(text=f"正在处理: {os.path.basename(pdf_path)} ({idx+1}/{total_files})")
            root.update_idletasks()

            # 处理 PDF -> JPG
            output_folder = pdf_to_images(pdf_path, output_dir, poppler_path)

            # 复制 PDF 到输出目录
            copy_pdf_to_output(pdf_path, output_folder)
        except Exception as e:
            messagebox.showerror("错误", f"处理文件时出错: {os.path.basename(pdf_path)}\n错误信息: {str(e)}")
            break  # 出现错误后停止处理

    messagebox.showinfo("完成", "PDF 转换完成！")
    progress['value'] = 0  # 重置进度条
    status_label.config(text="")

# 创建 GUI
root = tk.Tk()
root.title("PDF 批量导出 JPG 工具")

# 输入文件
tk.Label(root, text="选择 PDF 文件:").grid(row=0, column=0, padx=10, pady=10)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="选择", command=select_input_files).grid(row=0, column=2, padx=10, pady=10)

# 输出目录
tk.Label(root, text="输出文件夹:").grid(row=1, column=0, padx=10, pady=10)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="选择", command=select_output_dir).grid(row=1, column=2, padx=10, pady=10)

# 进度条和状态显示
progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

status_label = tk.Label(root, text="")
status_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

# 开始处理按钮
tk.Button(root, text="开始处理", command=process_pdfs).grid(row=4, column=1, pady=20)

root.mainloop()
