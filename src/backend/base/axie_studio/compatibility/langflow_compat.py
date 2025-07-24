"""
Compatibility layer for old langflow imports.
This module provides backward compatibility for existing workflows that still reference langflow modules.
"""

# Re-export axie_studio modules under langflow namespace for compatibility
import sys
from types import ModuleType

# Import the actual axie_studio modules
try:
    from axie_studio.base.prompts import api_utils as _api_utils
    from axie_studio.custom.custom_component import component as _component
    from axie_studio.interface.custom import custom_component as _custom_component
    from axie_studio.template.field import base as _field_base
    from axie_studio import inputs as _inputs
    from axie_studio import schema as _schema
except ImportError:
    # Fallback if modules don't exist
    _api_utils = None
    _component = None
    _custom_component = None
    _field_base = None
    _inputs = None
    _schema = None

def create_compatibility_modules():
    """Create compatibility modules for langflow imports."""
    
    # Create langflow module structure
    if 'langflow' not in sys.modules:
        langflow = ModuleType('langflow')
        sys.modules['langflow'] = langflow
    
    if 'langflow.base' not in sys.modules:
        langflow_base = ModuleType('langflow.base')
        sys.modules['langflow.base'] = langflow_base
        sys.modules['langflow'].base = langflow_base
    
    if 'langflow.base.prompts' not in sys.modules:
        langflow_base_prompts = ModuleType('langflow.base.prompts')
        sys.modules['langflow.base.prompts'] = langflow_base_prompts
        sys.modules['langflow.base'].prompts = langflow_base_prompts
    
    if 'langflow.base.prompts.api_utils' not in sys.modules and _api_utils:
        sys.modules['langflow.base.prompts.api_utils'] = _api_utils
        sys.modules['langflow.base.prompts'].api_utils = _api_utils
    
    if 'langflow.custom' not in sys.modules:
        langflow_custom = ModuleType('langflow.custom')
        sys.modules['langflow.custom'] = langflow_custom
        sys.modules['langflow'].custom = langflow_custom
    
    if 'langflow.custom.custom_component' not in sys.modules:
        langflow_custom_component = ModuleType('langflow.custom.custom_component')
        sys.modules['langflow.custom.custom_component'] = langflow_custom_component
        sys.modules['langflow.custom'].custom_component = langflow_custom_component
    
    if 'langflow.custom.custom_component.component' not in sys.modules and _component:
        sys.modules['langflow.custom.custom_component.component'] = _component
        sys.modules['langflow.custom.custom_component'].component = _component
    
    if 'langflow.interface' not in sys.modules:
        langflow_interface = ModuleType('langflow.interface')
        sys.modules['langflow.interface'] = langflow_interface
        sys.modules['langflow'].interface = langflow_interface
    
    if 'langflow.interface.custom' not in sys.modules:
        langflow_interface_custom = ModuleType('langflow.interface.custom')
        sys.modules['langflow.interface.custom'] = langflow_interface_custom
        sys.modules['langflow.interface'].custom = langflow_interface_custom
    
    if 'langflow.interface.custom.custom_component' not in sys.modules and _custom_component:
        sys.modules['langflow.interface.custom.custom_component'] = _custom_component
        sys.modules['langflow.interface.custom'].custom_component = _custom_component
    
    if 'langflow.template' not in sys.modules:
        langflow_template = ModuleType('langflow.template')
        sys.modules['langflow.template'] = langflow_template
        sys.modules['langflow'].template = langflow_template
    
    if 'langflow.template.field' not in sys.modules:
        langflow_template_field = ModuleType('langflow.template.field')
        sys.modules['langflow.template.field'] = langflow_template_field
        sys.modules['langflow.template'].field = langflow_template_field
    
    if 'langflow.template.field.base' not in sys.modules and _field_base:
        sys.modules['langflow.template.field.base'] = _field_base
        sys.modules['langflow.template.field'].base = _field_base
    
    if 'langflow.inputs' not in sys.modules and _inputs:
        sys.modules['langflow.inputs'] = _inputs
        sys.modules['langflow'].inputs = _inputs
    
    if 'langflow.schema' not in sys.modules and _schema:
        sys.modules['langflow.schema'] = _schema
        sys.modules['langflow'].schema = _schema

# Initialize compatibility modules when this module is imported
create_compatibility_modules()
