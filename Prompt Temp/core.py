from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
para = input("ENTER THE PARAGRAPH : ")

class movie(BaseModel):
    title: str
    release_year: int
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    Summary: str

parser = PydanticOutputParser(pydantic_object=movie)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
         Extract movie information from the paragraph 
         {format_instr}
            """,
        ),
        ("human", "{para}"),
    ]
)

final = prompt.invoke({"para": para, "format_instr": parser.get_format_instructions()})

response = model.invoke(final)
print(response.content)
