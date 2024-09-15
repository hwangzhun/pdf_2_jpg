from PIL import Image
import os

def jpg_to_pdf(jpg_files, output_dir):
    if not jpg_files or not output_dir:
        raise ValueError("JPG files and output directory must be specified.")
    
    # Create a PDF file name
    pdf_file_path = os.path.join(output_dir, "output.pdf")

    # Convert JPGs to a single PDF
    try:
        images = [Image.open(jpg_file).convert('RGB') for jpg_file in jpg_files]
        images[0].save(pdf_file_path, save_all=True, append_images=images[1:])
    except Exception as e:
        raise RuntimeError(f"Error converting JPGs to PDF: {e}")

    return pdf_file_path
