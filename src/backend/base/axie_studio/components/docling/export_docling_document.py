from typing import Any

from docling_core.types.doc import ImageRefMode

from axie_studio.base.data.docling_utils import extract_docling_documents
from axie_studio.custom import Component
from axie_studio.io import DropdownInput, HandleInput, MessageTextInput, Output, StrInput
from axie_studio.schema import Data, DataFrame


class ExportDoclingDocumentComponent(Component):
    display_name: str = "Export DoclingDocument"
    description: str = "Export DoclingDocument to markdown, html or other formats."
    documentation = "https://docling-project.github.io/docling/"
    icon = "Docling"
    name = "ExportDoclingDocument"

    inputs = [
        HandleInput(
            name="data_inputs",
            display_name="Data or DataFrame",
            info="The data with documents to export.",
            input_types=["Data", "DataFrame"],
            required=True,
        ),
        DropdownInput(
            name="export_format",
            display_name="Export format",
            options=["Markdown", "HTML", "Plaintext", "DocTags"],
            info="Select the export format to convert the input.",
            value="Markdown",
            real_time_refresh=True,
        ),
        DropdownInput(
            name="image_mode",
            display_name="Image export mode",
            options=["placeholder", "embedded"],
            info=(
                "Specify how images are exported in the output. Placeholder will replace the images with a string, "
                "whereas Embedded will include them as base64 encoded images."
            ),
            value="placeholder",
        ),
        StrInput(
            name="md_image_placeholder",
            display_name="Image placeholder",
            info="Specify the image placeholder for markdown exports.",
            value="<!-- image -->",
            advanced=True,
        ),
        StrInput(
            name="md_page_break_placeholder",
            display_name="Page break placeholder",
            info="Add this placeholder betweek pages in the markdown output.",
            value="",
            advanced=True,
        ),
        MessageTextInput(
            name="doc_key",
            display_name="Doc Key",
            info="The key to use for the DoclingDocument column.",
            value="doc",
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Exported data", name="data", method="export_document"),
        Output(display_name="DataFrame", name="dataframe", method="as_dataframe"),
    ]

    def update_build_config(self, build_config: dict, field_value: Any, field_name: str | None = None) -> dict:
        if field_name == "export_format" and field_value == "Markdown":
            build_config["md_image_placeholder"]["show"] = True
            build_config["md_page_break_placeholder"]["show"] = True
            build_config["image_mode"]["show"] = True
        elif field_name == "export_format" and field_value == "HTML":
            build_config["md_image_placeholder"]["show"] = False
            build_config["md_page_break_placeholder"]["show"] = False
            build_config["image_mode"]["show"] = True
        elif field_name == "export_format" and field_value in {"Plaintext", "DocTags"}:
            build_config["md_image_placeholder"]["show"] = False
            build_config["md_page_break_placeholder"]["show"] = False
            build_config["image_mode"]["show"] = False

        return build_config

    def export_document(self) -> list[Data]:
        documents = extract_docling_documents(self.data_inputs, self.doc_key)

        results: list[Data] = []
        try:
            image_mode = ImageRefMode(self.image_mode)
            for doc in documents:
                content = ""
                if self.export_format == "Markdown":
                    content = doc.export_to_markdown(
                        image_mode=image_mode,
                        image_placeholder=self.md_image_placeholder,
                        page_break_placeholder=self.md_page_break_placeholder,
                    )
                elif self.export_format == "HTML":
                    content = doc.export_to_html(image_mode=image_mode)
                elif self.export_format == "Plaintext":
                    content = doc.export_to_text()
                elif self.export_format == "DocTags":
                    content = doc.export_to_doctags()

                results.append(Data(text=content))
        except Exception as e:
            msg = f"Error splitting text: {e}"
            raise TypeError(msg) from e

        return results

    def as_dataframe(self) -> DataFrame:
        return DataFrame(self.export_document())
