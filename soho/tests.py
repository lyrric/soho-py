import asyncio

from soho import soho_http
from soho import views


async def test_get_free_activity_list():
    await views._check_token_id_scheduled('3423423423')


asyncio.run(test_get_free_activity_list())
