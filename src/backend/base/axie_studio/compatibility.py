"""
Compatibility layer for legacy Langflow imports.

This module ensures that existing code importing from 'langflow' continues to work
by creating aliases to the new 'axie_studio' module structure.
"""

import sys
from types import ModuleType


class LangflowCompatibilityModule(ModuleType):
    """A compatibility module that redirects langflow imports to axie_studio."""
    
    def __init__(self, name: str, axie_studio_module_name: str):
        super().__init__(name)
        self._axie_studio_module_name = axie_studio_module_name
        self._axie_studio_module = None
    
    def __getattr__(self, name: str):
        # Lazy load the axie_studio module
        if self._axie_studio_module is None:
            try:
                self._axie_studio_module = __import__(self._axie_studio_module_name, fromlist=[''])
            except ImportError:
                raise ImportError(f"Cannot import {self._axie_studio_module_name}")
        
        # Get the attribute from the axie_studio module
        return getattr(self._axie_studio_module, name)
    
    def __dir__(self):
        # Lazy load the axie_studio module
        if self._axie_studio_module is None:
            try:
                self._axie_studio_module = __import__(self._axie_studio_module_name, fromlist=[''])
            except ImportError:
                return []
        
        return dir(self._axie_studio_module)


def setup_langflow_compatibility():
    """Set up compatibility modules for langflow imports."""
    
    # Main langflow module
    if 'langflow' not in sys.modules:
        sys.modules['langflow'] = LangflowCompatibilityModule('langflow', 'axie_studio')
    
    # Core submodules that are commonly imported
    submodules = [
        'api',
        'components',
        'custom',
        'graph',
        'interface',
        'load',
        'schema',
        'services',
        'utils',
        'initial_setup',
        'logging',
        'middleware',
        'field_typing',
        'io',
        'events',
        'cli',
        'main',
        '__main__',
    ]
    
    for submodule in submodules:
        langflow_name = f'langflow.{submodule}'
        axie_studio_name = f'axie_studio.{submodule}'
        
        if langflow_name not in sys.modules:
            sys.modules[langflow_name] = LangflowCompatibilityModule(langflow_name, axie_studio_name)
    
    # Nested submodules that are commonly used
    nested_modules = [
        'langflow.api.v1',
        'langflow.components.data',
        'langflow.components.inputs',
        'langflow.components.outputs',
        'langflow.components.prompts',
        'langflow.components.agents',
        'langflow.components.chains',
        'langflow.components.embeddings',
        'langflow.components.llms',
        'langflow.components.memories',
        'langflow.components.retrievers',
        'langflow.components.textsplitters',
        'langflow.components.toolkits',
        'langflow.components.tools',
        'langflow.components.vectorstores',
        'langflow.custom.custom_component',
        'langflow.graph.vertex',
        'langflow.interface.components',
        'langflow.interface.initialize',
        'langflow.interface.utils',
        'langflow.schema.data',
        'langflow.schema.message',
        'langflow.schema.artifact',
        'langflow.services.database',
        'langflow.services.deps',
        'langflow.services.settings',
        'langflow.services.flow',
        'langflow.initial_setup.setup',
        'langflow.logging.logger',
    ]
    
    for nested_module in nested_modules:
        axie_studio_name = nested_module.replace('langflow.', 'axie_studio.')
        
        if nested_module not in sys.modules:
            sys.modules[nested_module] = LangflowCompatibilityModule(nested_module, axie_studio_name)


# Set up compatibility when this module is imported
setup_langflow_compatibility()
