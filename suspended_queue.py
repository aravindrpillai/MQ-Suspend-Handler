from messaging_api import MessagingAPI
import aiohttp
import asyncio
import time

async def ping_url(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_code = response.status
                if response_code >= 500:
                    return False
                elif response_code == 404:
                    return False
                return True
    except aiohttp.ClientError:
        return False

async def handle(app, app_url, message_id, dependancy_urls_array):
    can_resume = True
    while True:
        for url in dependancy_urls_array:
            url = url.strip()
            is_up = await ping_url(url)
            print(" MQ {}:{} -> dependancy url {} is {}".format(app, message_id, url, "UP" if is_up else "DOWN"))
            if(not is_up):
                can_resume = False

        if(can_resume):
            break
        time.sleep(10)
    
    messaging_api = MessagingAPI(app, app_url)
    has_resumed = await messaging_api.resume(message_id)
    print("MQ {}:{} -> Resumed Status: {} ".format(app, message_id, has_resumed))
    return has_resumed
    
def execute(app, app_url, message_id, dependancy_urls_array):
    return asyncio.run(handle(app, app_url, message_id, dependancy_urls_array))



# async def test2():
#     return await ping_url("http://lens35.in")

# print(asyncio.run(test2()))
