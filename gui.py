import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import sys
from pdf_to_jpg import pdf_to_images
from file_operations import copy_pdf_to_output
from jpg_to_pdf import jpg_to_pdf

def select_input_files(file_type, input_entry):
    if file_type == "pdf":
        input_files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    elif file_type == "jpg":
        input_files = filedialog.askopenfilenames(filetypes=[("JPG files", "*.jpg")])
    else:
        return
    if input_files:
        sorted_files = sorted(input_files, key=lambda x: os.path.basename(x))
        input_entry.delete(0, tk.END)
        input_entry.insert(0, ";".join(sorted_files))

def select_output_dir(output_entry):
    output_dir = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_dir)

def process_pdfs(input_entry, output_entry, progress, status_label):
    input_files = input_entry.get().split(";")
    output_dir = output_entry.get()

    if not input_files or not output_dir:
        messagebox.showerror("错误", "请选择输入文件和输出目录")
        return

    try:
        total_files = len(input_files)
        progress['maximum'] = total_files

        for idx, pdf_path in enumerate(input_files):
            progress['value'] = idx + 1
            status_label.config(text=f"正在处理: {os.path.basename(pdf_path)} ({idx+1}/{total_files})")
            status_label.update_idletasks()

            output_folder = pdf_to_images(pdf_path, output_dir)

            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            merged_folder = os.path.join(output_dir, f"{base_name}_合并")
            os.makedirs(merged_folder, exist_ok=True)

            copy_pdf_to_output(pdf_path, merged_folder)

    except Exception as e:
        messagebox.showerror("错误", f"处理文件时出错: {os.path.basename(pdf_path)}\n错误信息: {str(e)}")
        return

    messagebox.showinfo("完成", "PDF 转换完成！")
    progress['value'] = 0
    status_label.config(text="")

def process_jpgs(input_entry, output_entry, progress, status_label):
    input_files = input_entry.get().split(";")
    output_dir = output_entry.get()

    if not input_files or not output_dir:
        messagebox.showerror("错误", "请选择输入文件和输出目录")
        return

    try:
        sorted_files = sorted(input_files, key=lambda x: os.path.basename(x))
        base_name = os.path.splitext(os.path.basename(sorted_files[0]))[0]
        output_pdf = os.path.join(output_dir, f"{base_name}_合并.pdf")
        jpg_to_pdf(sorted_files, output_pdf)

    except Exception as e:
        messagebox.showerror("错误", f"处理文件时出错: {str(e)}")
        return

    messagebox.showinfo("完成", "JPG 转换为 PDF 完成！")
    progress['value'] = 0
    status_label.config(text="")

def start_gui():
    # 创建主窗口
    root = tk.Tk()
    root.title("PDF2JPG 批量转换工具 V1.1")
    root.iconbitmap('icon.ico')

    # Configure root grid layout to expand
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # 创建标签栏（Notebook）
    notebook = ttk.Notebook(root)
    tab_pdf_to_jpg = ttk.Frame(notebook)
    tab_jpg_to_pdf = ttk.Frame(notebook)

    notebook.add(tab_pdf_to_jpg, text="PDF 转 JPG")
    notebook.add(tab_jpg_to_pdf, text="JPG 转 PDF")
    notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Configure notebook to expand
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # --- PDF 转 JPG 标签内容 ---
    tab_pdf_to_jpg.columnconfigure(1, weight=1)
    tab_jpg_to_pdf.columnconfigure(1, weight=1)

    tk.Label(tab_pdf_to_jpg, text="选择 PDF 文件:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    input_entry_pdf = tk.Entry(tab_pdf_to_jpg, width=50)
    input_entry_pdf.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    tk.Button(tab_pdf_to_jpg, text="选择", command=lambda: select_input_files("pdf", input_entry_pdf)).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(tab_pdf_to_jpg, text="输出文件夹:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    output_entry_pdf = tk.Entry(tab_pdf_to_jpg, width=50)
    output_entry_pdf.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
    tk.Button(tab_pdf_to_jpg, text="选择", command=lambda: select_output_dir(output_entry_pdf)).grid(row=1, column=2, padx=10, pady=10)

    tk.Button(tab_pdf_to_jpg, text="开始处理", command=lambda: process_pdfs(input_entry_pdf, output_entry_pdf, progress, status_label)).grid(row=2, column=1, pady=20, sticky="ew")

    # --- JPG 转 PDF 标签内容 ---
    tk.Label(tab_jpg_to_pdf, text="选择 JPG 文件:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    input_entry_jpg = tk.Entry(tab_jpg_to_pdf, width=50)
    input_entry_jpg.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    tk.Button(tab_jpg_to_pdf, text="选择", command=lambda: select_input_files("jpg", input_entry_jpg)).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(tab_jpg_to_pdf, text="输出文件夹:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    output_entry_jpg = tk.Entry(tab_jpg_to_pdf, width=50)
    output_entry_jpg.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
    tk.Button(tab_jpg_to_pdf, text="选择", command=lambda: select_output_dir(output_entry_jpg)).grid(row=1, column=2, padx=10, pady=10)

    tk.Button(tab_jpg_to_pdf, text="开始处理", command=lambda: process_jpgs(input_entry_jpg, output_entry_jpg, progress, status_label)).grid(row=2, column=1, pady=20, sticky="ew")

    # 进度条和状态显示
    progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    status_label = tk.Label(root, text="")
    status_label.grid(row=2, column=0, padx=10, pady=5)

    # Footer: powered by hwangzhun
    footer_label = tk.Label(root, text="powered by hwangzhun", font=("Arial", 10), fg="gray")
    footer_label.grid(row=3, column=0, padx=10, pady=10, sticky='s')

    # Allow resizing of progress bar and footer
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=0)  # Progress bar
    root.rowconfigure(2, weight=0)  # Status label
    root.rowconfigure(3, weight=1)  # Footer

    root.mainloop()
