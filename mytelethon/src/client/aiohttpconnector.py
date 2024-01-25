from typing import Optional, Any
from socket import AF_INET
import ast
import aiohttp

SIZE_POOL_AIOHTTP = 100


class AiohttpConnector:
    aiohttp_client: Optional[aiohttp.ClientSession] = None

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP)
            cls.aiohttp_client = aiohttp.ClientSession(timeout=timeout, connector=connector)

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client is not None:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def method_post_to_url(cls, url: str, json_data) -> Any:
        client = cls.get_aiohttp_client()
        try:
            async with client.post(url, json=ast.literal_eval(json_data)) as response:
                if response.status != 200:
                    return {
                        'status': response.status,
                        'data': "AiohttpConnector:method_post_to_url: POST status {}".format(await response.text())
                    }
                json_result = await response.json()
        except Exception as e:
            return {
                'status': 500,
                'data': "AiohttpConnector:method_post_to_url: POST Exception {}".format(e)
            }
        # Если все прошло хорошо, должны получить url для qr-кода
        return {
            'status': 200,
            'data': json_result
        }

    @classmethod
    async def method_get_to_url(cls, url: str) -> Any:
        client = cls.get_aiohttp_client()
        try:
            async with client.get(url) as response:
                if response.status != 200:
                    return {
                        'status': response.status,
                        'data': "AiohttpConnector:method_get_to_url: GET status: {}".format(str(await response.text()))
                    }
                json_result = await response.json()
        except Exception as e:
            return {
                'status': 500,
                'data': "AiohttpConnector:method_to_url: GET Exception: {}".format(e)
            }
        # Если все прошло хорошо, должны получить url для qr-кода
        return {
            'status': 200,
            'data': json_result
        }
