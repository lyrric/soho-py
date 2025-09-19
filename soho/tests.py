import asyncio

from soho import soho_http
from soho.views import get_free_activity_list


async def test_get_free_activity_list():
    await soho_http.get_list('5de6501cda7417a260797555f4415516', False, "12:00")


asyncio.run(test_get_free_activity_list())
