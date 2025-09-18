import asyncio
from soho.views import get_free_activity_list


async def test_get_free_activity_list():
    result = await get_free_activity_list()
    print(result)


asyncio.run(test_get_free_activity_list())
