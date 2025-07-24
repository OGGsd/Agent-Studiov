from axie_studio.base.embeddings.aiml_embeddings import AIMLEmbeddingsImpl
from axie_studio.base.embeddings.model import LCEmbeddingsModel
from axie_studio.field_typing import Embeddings
from axie_studio.inputs.inputs import DropdownInput
from axie_studio.io import SecretStrInput


class AIMLEmbeddingsComponent(LCEmbeddingsModel):
    display_name = "AI/ML Embeddings"
    description = "Generate embeddings using the AI/ML API."
    icon = "AI/ML"
    name = "AIMLEmbeddings"

    inputs = [
        DropdownInput(
            name="model_name",
            display_name="Model Name",
            options=[
                "text-embedding-3-small",
                "text-embedding-3-large",
                "text-embedding-ada-002",
            ],
            required=True,
        ),
        SecretStrInput(
            name="aiml_api_key",
            display_name="AI/ML API Key",
            value="AIML_API_KEY",
            required=True,
        ),
    ]

    def build_embeddings(self) -> Embeddings:
        return AIMLEmbeddingsImpl(
            api_key=self.aiml_api_key,
            model=self.model_name,
        )
