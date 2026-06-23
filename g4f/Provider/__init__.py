from __future__ import annotations

from .. import debug
from ..providers.base_provider import AsyncGeneratorProvider, AsyncProvider
from ..providers.create_images import CreateImagesProvider
from ..providers.retry_provider import IterListProvider, RetryProvider, RotatedProvider
from ..providers.types import BaseProvider, ProviderType
from .needs_auth import *
from .needs_auth.hf import (
    HuggingChat,
    HuggingFace,
    HuggingFaceAPI,
    HuggingFaceInference,
    HuggingFaceMedia,
)

try:
    from .needs_auth.mini_max import HailuoAI, MiniMax
except (ImportError, SyntaxError) as e:
    debug.error("MiniMax providers not loaded:", e)

from .template import BackendApi, OpenaiTemplate

try:
    from .qwen.QwenCode import QwenCode
except (ImportError, SyntaxError) as e:
    debug.error("QwenCode provider not loaded:", e)
try:
    from .not_working import *
except (ImportError, SyntaxError) as e:
    debug.error("Not working providers not loaded:", e)
try:
    from .local import *
except (ImportError, SyntaxError) as e:
    debug.error("Local providers not loaded:", e)
try:
    from .hf_space import *
except (ImportError, SyntaxError) as e:
    debug.error("HuggingFace Space providers not loaded:", e)
try:
    from .audio import *
except (ImportError, SyntaxError) as e:
    debug.error("Audio providers not loaded:", e)
try:
    from .search import *
except (ImportError, SyntaxError) as e:
    debug.error("Search providers not loaded:", e)

import sys

from .ApiAirforce import ApiAirforce
from .Blackbox import Blackbox
from .Chatai import Chatai
from .Cloudflare import Cloudflare
from .Copilot import Copilot
from .DeepInfra import DeepInfra
from .deprecated.ARTA import ARTA
from .deprecated.DuckDuckGo import DuckDuckGo
from .EasyChat import EasyChat
from .GLM import GLM
from .Kimi import Kimi
from .LambdaChat import LambdaChat
from .Mintlify import Mintlify
from .OIVSCodeSer0501 import OIVSCodeSer0501
from .OIVSCodeSer2 import OIVSCodeSer2
from .OperaAria import OperaAria
from .PerplexityLabs import PerplexityLabs
from .PollinationsAI import PollinationsAI
from .PollinationsImage import PollinationsImage
from .Qwen import Qwen
from .Startnest import Startnest
from .TeachAnything import TeachAnything
from .WeWordle import WeWordle
from .Yqcloud import Yqcloud

__modules__: list = [
    getattr(sys.modules[__name__], provider)
    for provider in dir()
    if not provider.startswith("__")
]
__providers__: list[ProviderType] = [
    provider
    for provider in __modules__
    if isinstance(provider, type) and issubclass(provider, BaseProvider)
]
__all__: list[str] = [provider.__name__ for provider in __providers__]
__map__: dict[str, ProviderType] = {
    provider.__name__: provider for provider in __providers__
}


class ProviderUtils:
    convert: dict[str, ProviderType] = __map__
