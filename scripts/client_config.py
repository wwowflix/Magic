from __future__ import annotations

"""
Week 0 stub for scripts.client_config.

The original module depends on Selenium's webdriver.common.proxy.Proxy
and ProxyType. For smoke-import tests we only need a minimal surface
so this module can be imported without the real Selenium dependency.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ProxyType(Enum):
    """
    Minimal stand-in for Selenium's ProxyType enum.
    The exact values are not important for Week 0.
    """

    DIRECT = "direct"
    MANUAL = "manual"
    AUTODETECT = "autodetect"
    SYSTEM = "system"
    PAC = "pac"


@dataclass
class Proxy:
    """
    Minimal stand-in for Selenium's Proxy object.

    Only a small subset of attributes is provided to satisfy any
    light usage in higher-level code. For Week 0 we do not attempt
    to actually configure network proxies.
    """

    http_proxy: Optional[str] = None
    ssl_proxy: Optional[str] = None
    ftp_proxy: Optional[str] = None
    no_proxy: Optional[str] = None
    proxy_type: ProxyType = ProxyType.DIRECT


@dataclass
class ClientConfig:
    """
    Simple configuration holder for HTTP/S clients.

    This replaces the heavier Selenium-dependent logic for the purposes
    of import-time smoke tests.
    """

    base_url: str
    timeout: float = 30.0
    proxy: Optional[Proxy] = None


def default_client_config() -> ClientConfig:
    """
    Return a default client configuration instance.
    """
    return ClientConfig(base_url="http://localhost", timeout=30.0, proxy=None)
