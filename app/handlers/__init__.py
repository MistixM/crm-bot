# Drop the all routers here

from .start import start_router
from .message_handler import handler_message

routers = [start_router,

           # blocking routers must be at the end
           handler_message]