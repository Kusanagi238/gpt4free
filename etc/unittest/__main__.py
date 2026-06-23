import unittest

# Delay importing g4f.debug to avoid triggering import-time syntax errors
# (for example, when running under older Python versions that don't support
# certain syntax in provider modules). Catch import/SyntaxError to skip on
# unsupported environments.
try:
    import g4f.debug

    g4f.debug.version_check = False
except Exception:
    # If import fails (including SyntaxError on older Pythons), continue without g4f.debug
    pass

from .asyncio import *
from .backend import *
from .client import *
from .image_client import *
from .include import *
from .main import *
from .model import *
from .models import *
from .retry_provider import *
from .thinking import *
from .web_search import *

unittest.main()
