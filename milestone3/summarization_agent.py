
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from memory import create_memory

def create_summarization_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.2
    )

    prompt = PromptTemplate(
        input_variables=["research"],
        template="Summarize the following research concisely:\n{research}"
    )

    memory = create_memory()

    return LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory
    )
