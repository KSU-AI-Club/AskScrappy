import os
from typing import *

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

from rag.prompts import *
from utils.utils import *


# Nodes for Langgraph
class Node(TypedDict):
    question: str
    generation: str
    documents: List[str]

# Abstract Class (States)
class State:
    def __init__(self, llm, prompt):
        self.llm = llm
        self.prompt = prompt
        

class Retriever:
    def __init__(self, docs:List[str]):
        
        """
        Takes in a list of documents and determines whether the documents are 
        relevant to the question or not

        Args:
            llm (ChatOllama): Large Language Model (Llama 3.1)
            docs (List[str]): Documents for Vector Database
            prompt (PromptTemplate): Prompt for Retriever
        """
        self.retriever = self.__load_vectorstore(docs)
        
    def __load_vectorstore(self, docs):
        vectorstore = Chroma.from_documents(documents=docs,
                                     collection_name="askscrappy-db",
                                     embedding=OpenAIEmbeddings())
        
        return vectorstore.as_retriever(search_kwargs={"k": 10})

    def __call__(self, state):
        question = state["question"]
        relevant_docs = self.retriever.get_relevant_documents(question)
        
        return {"documents": relevant_docs, "question": question}
      
        
class Generator(State):
    def __init__(self, llm: ChatOllama, prompt: PromptTemplate):
        """
        Generates Response based on the Retrieved Documents from the Retriver State

        Args:
            llm (ChatOllama): Large Language Model (Llama 3.1)
            prompt (PromptTemplate): Prompt for Generator
        """
        super().__init__(llm, prompt)
        self.rag_chain = prompt | llm | StrOutputParser()
    
    def __call__(self, state):
        
        question = state["question"]
        documents = state["documents"]
        
        generation = self.rag_chain.invoke({"context": documents, "question": question})
        return {"documents": documents, "question": question, "generation": generation}
        

class DocumentGrader(State):
    def __init__(self, llm: ChatOllama, prompt: PromptTemplate):
        """
        Determines How well the Documents Retrieved from the VectorStore are relevent to the question

        Args:
            llm (ChatOllama): Large Language Model
            prompt (PromptTemplate): Prompt Template
        """
        super().__init__(llm, prompt)
        self.grader = prompt | llm | JsonOutputParser()
    
    def __call__(self, state):
        question = state["question"]
        documents = state["documents"]
        
        filtered_docs = []
        
        for d in documents:
            grade = self.grader.invoke({"question": question, 
                                                 "document": d.page_content})
            if grade["score"] == "yes":
                filtered_docs.append(d)
                
        return {"documents": filtered_docs, "question": question}


class TransformQuery(State):
    def __init__(self, llm: ChatOllama, prompt: PromptTemplate):
        """
        Transforms the Original User's question to hopefully get a better query  

        Args:
            llm (ChatOllama): Large Language Model
            prompt (PromptTemplate): PromptTemplate
        """
        super().__init__(llm, prompt)
        self.question_rewriter = prompt | llm | StrOutputParser()
    
    def __call__(self, state):
        question = state["question"]
        documents = state["documents"]
        
        rewritten_question = self.question_rewriter.invoke({"question": question})
        return {"documents": documents, "question": rewritten_question}

# Edges
# ========================= #
class AnswerGrader(State):
    def __init__(self, llm: ChatOllama, prompt: PromptTemplate):
        """
        Grades the response of the generated answer

        Args:
            llm (ChatOllama): Large Language Model
            prompt (PromptTemplate): PromptTemplate
        """
        super().__init__(llm, prompt)
        self.a_grader = prompt | llm | JsonOutputParser()
    
    def __call__(self, state: Node):
        question = state["question"]
        generation = state["generation"]
        
        return self.a_grader.invoke({"question":question, "generation": generation})
    

class HallucinationGrader(State):
    def __init__(self, llm, prompt):
        """
        Checks the LLM's generated output to see whether there are hallucincations or not

        Args:
            llm (ChatOllama): Large Language Model
            prompt (PromptTemplate): PromptTemplate
        """
        super().__init__(llm, prompt)
        self.h_grader = prompt | llm | JsonOutputParser()
        
        
    def __call__(self, state: Node):
        documents = state["documents"]
        generation = state["generation"]
        
        return self.h_grader.invoke({"documents":documents, "generation": generation})

def decide_to_generate(state: Node) -> str:
    """
    A conditional edge to determine whether to generate a response or not based on the number of filter docs
    No filter documents -> Transform the query

    Else: 
        Generate a Response based on the filtered docs

    Args:
        state (State): 

    Returns:
        str: which node to go to [transform_query, generate]
    """
    filtered_docs = state["documents"]
    
    if not filtered_docs:
        return "transform_query"
    
    else:
        return "generate"
    
    
def check_hallucincations(state: State) -> str:
    """Determines whether there are hallunications or no

    Args:
        state (State): _description_

    Returns:
        _type_: _description_
    """
    
    local_llm = ChatOllama(model="llama3.1", 
                           format="json",
                           temperature=0)
    
    hallucincation_grader = HallucinationGrader(local_llm, 
                                                prompts["hallucination_grader"])
    answer_grader = AnswerGrader(local_llm, 
                                 prompts["answer_grader"])
    
    score = hallucincation_grader(state)
    grade = score["score"]
    
    if grade == "yes":     
        score = answer_grader(state)
        grade = score["score"]
        
        if grade == "yes":
            return "useful"
        
        else: 
            return "not useful"
    else:
        return "not supported"  

def create_rag_model(docs):
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    
    local_llm = ChatOllama(model="llama3.1", 
                           format="json", 
                           temperature=0)
    generator_llm = ChatOllama(model="llama3.1", temperature=0)
    
    retriever = Retriever(docs)
    generator = Generator(generator_llm, prompts["generator"])
    doc_grader = DocumentGrader(local_llm, prompts["doc_grader"])
    transform_query = TransformQuery(local_llm, prompts["rewritten_grader"])
    
    workflow = StateGraph(Node)
    
    # Define the nodes
    workflow.add_node("retrieve", retriever)  # retrieve
    workflow.add_node("grade_documents", doc_grader)  # grade documents
    workflow.add_node("generate", generator)  # generatae
    workflow.add_node("transform_query", transform_query)  # transform_query

    # Build graph
    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "transform_query": "transform_query",
            "generate": "generate",
        },
    )
    workflow.add_edge("transform_query", "retrieve")
    
    # Modify the edge such that
    workflow.add_conditional_edges(
        "generate",
        check_hallucincations,
        {
            "not supported": "generate",
            "useful": END,
            "not useful": "transform_query",
        },
    )
    
    return workflow.compile()