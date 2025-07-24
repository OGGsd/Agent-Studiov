"""
Legacy Langflow CLI entry point.
Redirects to axie_studio.__main__ for backward compatibility.
"""

import warnings

# Issue deprecation warning
warnings.warn(
    "Using 'python -m langflow' is deprecated. Please use 'python -m axie_studio' instead. "
    "This compatibility layer will be maintained for backward compatibility.",
    DeprecationWarning,
    stacklevel=2
)

# Import and run the axie_studio main
from axie_studio.__main__ import main

if __name__ == "__main__":
    main()
