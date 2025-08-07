import os
try:
    from docx import Document
except ImportError:
    print("python-docx not installed. Installing...")
    os.system("pip install python-docx")
    from docx import Document

def read_docx_file(file_path):
    """Read a DOCX file and extract text content"""
    try:
        doc = Document(file_path)
        text_content = []
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_content.append(paragraph.text)
        
        return '\n'.join(text_content)
    except Exception as e:
        return f"Error reading {file_path}: {str(e)}"

# Files to read
files_to_read = [
    "decennium descent player rulebook.docx",
    "The Cosmology of Decennium Descent.docx", 
    "The_World_of_Aethel_Lore.docx"
]

for file_name in files_to_read:
    print(f"\n{'='*60}")
    print(f"READING: {file_name}")
    print(f"{'='*60}")
    
    content = read_docx_file(file_name)
    print(content)
    print(f"\n{'='*60}")
    print(f"END OF: {file_name}")
    print(f"{'='*60}\n")