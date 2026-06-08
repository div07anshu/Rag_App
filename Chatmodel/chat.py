from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from transformers.utils import logging

load_dotenv()
logging.set_verbosity_error()

llm = HuggingFacePipeline.from_model_id(
    model_id="Qwen/Qwen2.5-1.5B-Instruct",
    task="text-generation",
    pipeline_kwargs=dict(
        max_new_tokens=524,
        do_sample=True,
        repetition_penalty=1.03,
        return_full_text=False,
    ),
)

model = ChatHuggingFace(llm=llm)


messages = [
    SystemMessage(
        content="you are interactive ai agent .."
    )
]

print("Enter 0 to stop the chatting......")

while 1:
    data = input("You : ")
    messages.append(HumanMessage(content=data)) # type: ignore
    if data == "0":
        break

    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content)) # pyright: ignore[reportArgumentType]
    print("AI : ",response.content)

print(messages)