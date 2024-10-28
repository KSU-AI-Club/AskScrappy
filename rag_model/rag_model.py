import glob
import os
import time
from typing import *

from uuid import uuid4
from dotenv import load_dotenv

from langchain.load import dumps, loads
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryByteStore

ROOT_DIR = "docs/"
PERSIST_DIR = "vector_db"

"""
Check if there is a already loaded Vector Database
If not, -->  use load document 

Lowering Temperature Results in Lower chance of AI hallucincations

1. Query -> 
    Rewrite Query into Different Perspectives and Make it be specific -> Combine Documents -> Return Documents for VectorStore

    
2. Indexing -> 
    Create Summarization of the Documents -> Store Summarization into Vector Store -> Store Original Documents Into DocStore
    
3. Routing -> 
    
"""

def get_unique_union(documents: list[list]):
    """ 
    Unique union of retrieved docs 
    """
    
    # Flatten list of lists, and convert each Document to string
    flattened_docs = [dumps(doc) for sublist in documents for doc in sublist]
    
    unique_docs = list(set(flattened_docs))
    return [loads(doc) for doc in unique_docs]

def multi_query(llm: OpenAI):
     
    template = """ You are a review critic on the different perspectives of how questions can be analyzed
    
    Looking at this question: {question}
    Name 5 ways this question can be analyzed and rewritten as?
    Provide these alternative questions separated by newlines and add no leading descriptions.
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    generate_queries = (prompt 
             | llm 
             | StrOutputParser() 
             | (lambda x: x.split("\n")))
    
    return generate_queries

def load_documents(root_dir:str, retriever:MultiVectorRetriever, approach: Literal["split", "summary"]="split") -> None:
    """
    Loads text documents from a directory into a Chroma Vector Database
    
    1. Vector DB for Major and Class Information
    2. Relational DB for Teacher Performance and Evaluation

    Args:
        root_dir (str): the root_directory of all KSU AI Documents
        retriever (MultiVectorRetriever): Multi-Vector Retriever that contains both the split or summarized documents and the original documents
        approach (tuple, optional): Determines what whether the documents be split into sub documents or the documents be summarized . Defaults to ("summary", "split").
    """
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=50)
    pdf_document_paths = glob.glob(f"{root_dir}**/*.pdf", recursive=True)
    
    assert approach.lower() in ("summary", "split"), "Approach needs to be either \"summary\" or \"split\"" 
    
    if approach.lower() == "split":
         
        sub_doc_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=10)
        sub_docs = []
        
        for i, pdf_doc_path in enumerate(pdf_document_paths):
            loaded_pdf_docs = PyPDFLoader(pdf_doc_path)
            pdf_docs = text_splitter.split_documents(loaded_pdf_docs.load()) 
            doc_uuids = [str(uuid4()) for _ in pdf_docs]
            
            sub_doc_id = doc_uuids[i]
            
            for pdf_doc in pdf_docs:
                sub_pdf_docs = sub_doc_splitter.split_documents([pdf_doc])
                
                for sub_pdf_doc in sub_pdf_docs:
                    sub_pdf_doc.metadata["doc_id"] = sub_doc_id
                
                sub_docs.extend(sub_pdf_docs)
                retriever.vectorstore.add_documents(documents=sub_pdf_docs)
            
            retriever.docstore.mset(list(zip(doc_uuids, pdf_docs)))
            
    else:
        #TODO Implement this for summarizing documents instead of splitting documents
        llm = OpenAI(temperature=0.1)
        
def prompt() -> None:
     
    template = """
    You are KSU's primary advisor for uncoming students
    context: {context},
    
    be as specific as possible
    list out all the course names, course name ids, and its prerequisite for taking the course
    Reply to the student's statement or question: {question}, Think Carefully.
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    return prompt

def llm_chain(multi_query_chain, 
              retriever:MultiVectorRetriever, 
              prompt: ChatPromptTemplate, 
              llm: OpenAI):
    """
    Creates a langchain connection the Vector Databse to the LLM

    Args:
        retriever (Chroma): chroma retriever
        prompt (ChatPromptTemplate): chat prompt
        llm (OpenAI): large language model (from OpenAI)
    """
    
    # Returns a list of documents
    rag_chain = (
        multi_query_chain
        | retriever.map()
        | get_unique_union
    )

    # Returns the output
    output_chain = (
        {"context": rag_chain, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return output_chain

def ask_scrappy(question:str) -> str:

    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    
    
    summary_vector_store = Chroma(
            collection_name="summaries",
            embedding_function=OpenAIEmbeddings(),
            persist_directory=PERSIST_DIR)
    
    store = InMemoryByteStore()
    id_key = "doc_id"
    
    summary_retriever= MultiVectorRetriever(
        vectorstore=summary_vector_store,
        byte_store=store,
        id_key=id_key,
    )
    
    llm = OpenAI(model="gpt-4o-mini", temperature=0.4)
    llm_prompt = prompt()

    multi_query_chain = multi_query(llm)
    rag_chain = llm_chain(multi_query_chain, summary_retriever, llm_prompt, llm)

    output = rag_chain.invoke(question)
    
    return output

def main():
    question = input("Question: ")
    
    start = time.time()
    answer = ask_scrappy(question)
    end = time.time()
    print(f"Output: {answer}\nOutput Time: {end - start}")
    
    
if __name__ == "__main__":
    main()