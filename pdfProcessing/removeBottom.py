import fitz
import cv2
import numpy as np
import os


# literally remove bottom 100 pixels of all pages in a pdf (watermark)
def clean_pdf_watermarks(input_file="test.pdf", output_file="cleaned.pdf", bottom_pixels=100):
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return False
    
    try:
        doc = fitz.open(input_file)
        print(f"Processing PDF with {len(doc)} pages...")
        
        for page_num in range(len(doc)):
            page = doc[page_num]

            pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))

            if pix.n == 4:  # RGBA
                img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 4)
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            else:  # RGB
                img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            
            img[-bottom_pixels:, :] = [255, 255, 255]
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            success, buf = cv2.imencode('.png', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            if not success:
                print(f"Failed to encode page {page_num + 1}")
                continue

            img_doc = fitz.open("png", buf.tobytes())
            img_page = img_doc[0]

            page.clean_contents()
            page_rect = page.rect
            page.insert_image(page_rect, stream=buf.tobytes(), keep_proportion=True)
            
            img_doc.close()
            print(f"Processed page {page_num + 1}/{len(doc)}")
        
        doc.save(output_file)
        doc.close()
        print(f"Successfully saved cleaned PDF as '{output_file}'")
        return True
        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return False


if __name__ == "__main__":
    clean_pdf_watermarks()
