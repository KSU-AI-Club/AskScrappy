import glob
import PyPDF2

from typing import *
from langchain_community.document_loaders import TextLoader


def retrieve_pdf_docs(pdf_docs_path):
    return glob.glob(f"{pdf_docs_path}**/*.pdf", recursive=True)

def retrieve_txt_docs(txt_docs_path):
    return [TextLoader(txt_path, encoding = 'UTF-8').load() for txt_path in glob.glob(f"{txt_docs_path}*.txt")]

def pdf_to_txt_docs(root_path: str, txt_docs_path : str)-> List[str]:
    """
    Converts pdf to txt docs

    Args:
        root_path (str): root path of pdf files
        txt_docs_path (str): path of txt file paths (where you want to save)

    Returns:
        List[str]: List of text files
    """
    txt_docs = []
    pdf_doc_paths = retrieve_pdf_docs(root_path)
    print(pdf_doc_paths)
    for pdf_path in pdf_doc_paths:
        
        with open(pdf_path, "rb") as pdf_doc:
            pdf_reader = PyPDF2.PdfReader(pdf_doc)
            
            text = ''

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        
        text_path = f"{txt_docs_path}/{pdf_path.split("\\")[-1][:-4]}.txt"
        
        with open(text_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text) 
            # print(os.path.exists(text_path))
            txt_docs.append(TextLoader(text_path, encoding = 'UTF-8').load())
    
    return txt_docs

    
if __name__ == "__main__":
    
    # Converting pdfs to txt file
    root_path = "./output/"
    txt_docs_path = "./text_docs/"
    
    pdf_to_txt_docs(root_path, txt_docs_path)