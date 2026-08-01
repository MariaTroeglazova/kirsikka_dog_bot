from .common import router as common_router
from .profile import router as profile_router
from .debug import router as debug_router

__all__ = ["common_router", "profile_router", "debug_router"]