import argparse
import warnings

from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.nodes import *
from rag.prompts import *
from utils.utils import *

from pprint import pprint


def parser():
    parser = argparse.ArgumentParser(description="Parser for controlling Self-RAG Model")
    
    parser.add_argument("--temp", 
                        type=float, 
                        help="Sets the temperatures for the LLM",
                        default=0.1)
    
    parser.add_argument("--model", 
                        choices=["llama3.1", "llama3.2", "llama3.3"],
                        type=str,
                        help="Determines which type of LLM used for Self-RAG Model",
                        default="llama3.1")
    
    parser.add_argument("--embedding",
                        choices=["OpenAI", "BlackRock"],
                        type=str,
                        help="Sets the type of embedding used to embed the documents for vectorstore",
                        default="OpenAI")
    
    parser.add_argument("--vectorstore",
                        choices=["Chroma", "BlackRock"],
                        type=str,
                        help="Sets the type of vectorstore used for indexing and retrival",
                        default="Chroma")
    
    parser.add_argument("--root_path",
                        type=str,
                        help="Determines which path all the txt documents are located at",
                        default="./text_docs/")
    
    parser.add_argument("--chunk_size", 
                        type=int,
                        help="Sets the chunk size for the TextSplitter",
                        default=500)
    
    parser.add_argument("--chunk_overlap", 
                        type=int,
                        help="Sets the chunk overlap for the TextSplitter",
                        default=20)
    
    parser.add_argument("--question", 
                        type=str,
                        help="ask the question to the self-RAG model")
    
    args = parser.parse_args()
    
    return args

#TODO: Link args to main file


def split_docs(args):
    docs = retrieve_txt_docs(args.root_path)
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap)
    
    doc_splits = text_splitter.split_documents(docs_list)
    
    return doc_splits


def main():
    
    warnings.filterwarnings("ignore")

    args = parser()
    doc_splits = split_docs(args)
    app = create_rag_model(doc_splits)
    
    # TODO: Add ability to ask question in a better format then this welp
    inputs = {"question": "What prerequisites are required to take CS4277 and CS4306?"}
    for output in app.stream(inputs):
        for key, value in output.items():
            # Node
            # pprint(f"Node '{key}':")
            # Optional: print full state at each node
            pprint(value, indent=2, width=80, depth=None)
        pprint("\n---\n")

    # Final generation, Return output for backend 
    pprint(value["generation"])

if __name__ == "__main__":
    main()   