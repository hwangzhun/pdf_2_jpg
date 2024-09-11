import shutil
import os

def copy_pdf_to_output(pdf_path, output_dir):
    # 确保输出目录存在
    pdf_name = os.path.basename(pdf_path)
    output_path = os.path.join(output_dir, pdf_name)
    
    # 复制 PDF 文件
    shutil.copy(pdf_path, output_path)
