import os
from pypdf import PdfReader

def extract_text_from_pdfs(docs_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for filename in os.listdir(docs_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(docs_dir, filename)
            txt_filename = filename.replace('.pdf', '.txt')
            txt_path = os.path.join(output_dir, txt_filename)
            
            print(f"Extracting: {filename}...")
            try:
                reader = PdfReader(pdf_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Saved to: {txt_path}")
            except Exception as e:
                print(f"Error extracting {filename}: {e}")

if __name__ == "__main__":
    docs_dir = 'docs'
    output_dir = 'docs/extracted_text'
    extract_text_from_pdfs(docs_dir, output_dir)
