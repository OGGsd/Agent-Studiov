from axie_studio.components.data import FileComponent
from axie_studio.components.input_output import ChatInput, ChatOutput
from axie_studio.components.models import LanguageModelComponent
from axie_studio.components.processing import PromptComponent
from axie_studio.graph import Graph


def document_qa_graph(template: str | None = None):
    if template is None:
        template = """Answer user's questions based on the document below:

---

{Document}

---

Question:
{Question}

Answer:
"""
    file_component = FileComponent()

    chat_input = ChatInput()
    prompt_component = PromptComponent()
    prompt_component.set(
        template=template,
        context=file_component.load_files_message,
        question=chat_input.message_response,
    )

    openai_component = LanguageModelComponent()
    openai_component.set(input_value=chat_input.message_response, system_message=prompt_component.build_prompt)

    chat_output = ChatOutput()
    chat_output.set(input_value=openai_component.text_response)

    return Graph(start=chat_input, end=chat_output)
