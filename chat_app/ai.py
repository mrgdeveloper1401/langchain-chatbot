from pathlib import Path
import os
import openai
from langchain_community.document_loaders import PyPDFLoader

BASE_DIR = Path(__file__).resolve().parent.parent


my_file = BASE_DIR / "test_file" / "5-mohammad.pdf"

def langchain_pdf_file(file):
    loader = PyPDFLoader(file).load()
    return loader
