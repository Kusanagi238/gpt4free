from __future__ import annotations

import logging
import os
from typing import Coroutine, Optional, Union

from . import debug, version
from .client import AsyncClient, Client
from .cookies import get_cookies, set_cookies
from .models import Model
from .typing import AsyncResult, CreateResult, ImageType, Messages

# Guard provider imports so that importing this package does not execute provider implementation
# modules at import time (which can raise SyntaxError or other exceptions on some runtimes).
try:
    from .client.service import get_model_and_provider
    from .providers.helper import async_concat_chunks, concat_chunks
    from .providers.types import ProviderType
except Exception:
    # Providers may fail to import (for example a provider package using top-level `await`
    # on environments that don't support it). Provide fallbacks that raise clear errors
    # when used instead of failing during package import.
    ProviderType = None

    def concat_chunks(*args, **kwargs):
        raise RuntimeError(
            "providers.helper is not available; import failed or providers are not supported in this environment"
        )

    async def async_concat_chunks(*args, **kwargs):
        raise RuntimeError(
            "providers.helper is not available; import failed or providers are not supported in this environment"
        )

    def get_model_and_provider(*args, **kwargs):
        raise RuntimeError(
            "client.service.get_model_and_provider is not available; import failed or providers are not supported in this environment"
        )


# Configure logger
logger = logging.getLogger("g4f")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logger.addHandler(handler)
logger.setLevel(logging.ERROR)


class ChatCompletion:
    @staticmethod
    def _prepare_request(
        model: Union[Model, str],
        messages: Messages,
        provider: Union[ProviderType, str, None],
        stream: bool,
        image: ImageType,
        image_name: Optional[str],
        ignore_working: bool,
        ignore_stream: bool,
        **kwargs,
    ):
        """Shared pre-processing for sync/async create methods."""
        if image is not None:
            kwargs["media"] = [(image, image_name)]
        elif "images" in kwargs:
            kwargs["media"] = kwargs.pop("images")

        model, provider = get_model_and_provider(
            model,
            provider,
            stream,
            ignore_working,
            ignore_stream,
            has_images="media" in kwargs,
        )

        if "proxy" not in kwargs:
            proxy = os.environ.get("G4F_PROXY")
            if proxy:
                kwargs["proxy"] = proxy
        if ignore_stream:
            kwargs["ignore_stream"] = True

        return model, provider, kwargs

    @staticmethod
    def create(
        model: Union[Model, str],
        messages: Messages,
        provider: Union[ProviderType, str, None] = None,
        stream: bool = False,
        image: ImageType = None,
        image_name: Optional[str] = None,
        ignore_working: bool = False,
        ignore_stream: bool = False,
        **kwargs,
    ) -> Union[CreateResult, str]:
        model, provider, kwargs = ChatCompletion._prepare_request(
            model,
            messages,
            provider,
            stream,
            image,
            image_name,
            ignore_working,
            ignore_stream,
            **kwargs,
        )
        result = provider.create_function(model, messages, stream=stream, **kwargs)
        return result if stream or ignore_stream else concat_chunks(result)

    @staticmethod
    def create_async(
        model: Union[Model, str],
        messages: Messages,
        provider: Union[ProviderType, str, None] = None,
        stream: bool = False,
        image: ImageType = None,
        image_name: Optional[str] = None,
        ignore_working: bool = False,
        ignore_stream: bool = False,
        **kwargs,
    ) -> Union[AsyncResult, Coroutine[str]]:
        model, provider, kwargs = ChatCompletion._prepare_request(
            model,
            messages,
            provider,
            stream,
            image,
            image_name,
            ignore_working,
            ignore_stream,
            **kwargs,
        )
        result = provider.async_create_function(
            model, messages, stream=stream, **kwargs
        )
        if not stream and not ignore_stream and hasattr(result, "__aiter__"):
            result = async_concat_chunks(result)
        return result
