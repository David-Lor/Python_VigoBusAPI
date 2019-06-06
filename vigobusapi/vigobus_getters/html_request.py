
# # Native # #
from asyncio import wait_for

# # Installed # #
from requests_async import get, Response

# # Project # #
from vigobusapi.settings_handler import load_settings
from vigobusapi.settings_handler.const import *


settings = load_settings()


async def request_html(stopid: int) -> str:
    """Async function to request the webpage data source, returning the HTML content.
    :raises: asyncio.TimeoutError | requests_async.HTTPError
    """
    response: Response = await wait_for(get(settings[HTTP_REMOTE_API] + str(stopid)), timeout=settings[HTTP_TIMEOUT])
    response.raise_for_status()
    return response.text