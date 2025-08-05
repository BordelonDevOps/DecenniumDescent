from docx import Document
import docx2txt
import os

def read_docx_file(file_path):
    """Read and extract text content from a DOCX file"""
    try:
        doc = Document(file_path)
        content = []
        
        print(f"\n{'='*60}")
        print(f"Reading: {os.path.basename(file_path)}")
        print(f"{'='*60}")
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():  # Only add non-empty paragraphs
                content.append(paragraph.text)
                print(paragraph.text)
        
        return content
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return []

def read_doc_file(file_path):
    """Read and extract text content from a DOC file"""
    try:
        print(f"\n{'='*60}")
        print(f"Reading: {os.path.basename(file_path)}")
        print(f"{'='*60}")
        
        text = docx2txt.process(file_path)
        content = [line.strip() for line in text.split('\n') if line.strip()]
        
        for line in content:
            print(line)
        
        return content
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return []

def main():
    # List of DOCX files to read
    file_paths = [
        r'C:\Users\cbord\OneDrive\Documents\GitHub\Arena Fighter\decennium descent player rulebook.docx'
    ]
    
    all_content = {}
    
    for file_name in file_paths:
        if os.path.exists(file_name):
            if file_name.endswith('.docx'):
                content = read_docx_file(file_name)
            elif file_name.endswith('.doc'):
                content = read_doc_file(file_name)
            else:
                print(f"Unsupported file format: {file_name}")
                continue
            all_content[file_name] = content
        else:
            print(f"File not found: {file_name}")
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for file_name, content in all_content.items():
        print(f"{file_name}: {len(content)} paragraphs")

if __name__ == "__main__":
    main()