from docx import Document
import os

def read_backgrounds():
    try:
        doc = Document('Backgrounds.docx')
        print(f'Reading: {os.path.basename("Backgrounds.docx")}')
        print('='*60)
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                print(paragraph.text)
                
    except Exception as e:
        print(f'Error reading Backgrounds.docx: {str(e)}')

if __name__ == '__main__':
    read_backgrounds()