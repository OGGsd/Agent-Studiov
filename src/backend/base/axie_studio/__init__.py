"""Axie Studio - Professional AI Workflow Platform"""

__version__ = "1.0.0"

# Import compatibility layer for legacy langflow imports
try:
    from . import compatibility
except ImportError:
    pass