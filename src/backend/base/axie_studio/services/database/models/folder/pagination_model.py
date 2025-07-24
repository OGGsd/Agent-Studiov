from fastapi_pagination import Page

from axie_studio.helpers.base_model import BaseModel
from axie_studio.services.database.models.flow.model import Flow
from axie_studio.services.database.models.folder.model import FolderRead


class FolderWithPaginatedFlows(BaseModel):
    folder: FolderRead
    flows: Page[Flow]
