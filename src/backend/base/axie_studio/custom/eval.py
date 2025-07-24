from typing import TYPE_CHECKING

# Import compatibility layer early to ensure langflow modules are available
try:
    from axie_studio.compatibility import langflow_compat
    langflow_compat.create_compatibility_modules()
except ImportError:
    pass

from axie_studio.utils import validate

if TYPE_CHECKING:
    from axie_studio.custom.custom_component.custom_component import CustomComponent


def eval_custom_component_code(code: str) -> type["CustomComponent"]:
    """Evaluate custom component code."""
    class_name = validate.extract_class_name(code)
    return validate.create_class(code, class_name)
