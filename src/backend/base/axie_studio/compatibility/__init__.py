"""
Compatibility layer for legacy langflow imports.
"""

from .langflow_compat import create_compatibility_modules

# Automatically create compatibility modules when this package is imported
create_compatibility_modules()
