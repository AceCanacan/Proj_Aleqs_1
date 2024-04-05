import pandas as pd
import openai
import llama_index
import streamlit as st

import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from IPython.display import Markdown, display
import chromadb

import os
from dotenv import load_dotenv
import openai

# Absolute path to your .env file
env_path = '../.env'
load_dotenv(dotenv_path=env_path)

# Accessing the API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# load from disk
db2 = chromadb.PersistentClient(path="../pipeline/chroma_db")
chroma_collection = db2.get_or_create_collection("quickstart")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(
    vector_store,
    embed_model=embed_model,
)

query_engine = index.as_query_engine()

# Streamlit app starts here
st.title("Legal Querying System")

# Text input box where users can enter their query
user_query = st.text_input("Enter your query here:", "")

if st.button("Submit"):
    # Processing the user's input
    if user_query:  # making sure the input is not empty
        # Perform the query
        response_object = query_engine.query(user_query)
        
        # Extract the response text from the response object
        response_text = response_object.response
        
        # Display the response text
        st.write(response_text)
    else:
        st.write("Please enter a query to get a response.")

