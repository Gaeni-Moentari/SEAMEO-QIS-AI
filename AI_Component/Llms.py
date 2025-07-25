from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

# Load ENV and API's
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API Key tidak ditemukan. Pastikan file .env memiliki OPENAI_API_KEY yang valid.")

groqapi_key = os.getenv('groqapi_key')
if not groqapi_key:
    raise ValueError("Groq API key tidak ditemukan")

# LLMS 

##ollama
ollama = ChatOpenAI(
    model= "ollama/crewai-llama3.2",
    base_url = "http://localhost:11434/v1"
)

##OpenAI 
openai = ChatOpenAI(
    model='gpt-4o',
    temperature=0.3,
    api_key = api_key
)

##Groq
os.environ["GROQ_API_KEY"] = groqapi_key
groq = ChatOpenAI(
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=os.environ['GROQ_API_KEY'],
    model_name="groq/llama-3.2-3b-preview",
    temperature=0,
)

print("instance succesfully created!")
