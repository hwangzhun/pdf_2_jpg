from pdf2image import convert_from_path
import os

def pdf_to_images(pdf_path, output_dir, poppler_path):
    # 确保输出目录存在
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join(output_dir, pdf_name)
    os.makedirs(output_folder, exist_ok=True)

    # 将 PDF 转换为图片并保存为 JPG
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"{pdf_name}_page_{i + 1}.jpg")
        image.save(image_path, "JPEG")
    
    return output_folder
