import httpx
import asyncio
import time
from ..core.logger import logger

class MonitorService:

    async def check_single_url(self, address):
        try:
            start = time.time()

            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(address)

            end = time.time()

            response_time = int((end - start) * 1000)

            status = "UP" if 200 <= response.status_code < 300 else "DOWN"

            reason = None if status == "UP" else f"HTTP {response.status_code}"

            if status == "UP":
                logger.info(f"{address} UP {response_time}ms")
            else:
                logger.warning(f"{address} DOWN {reason}")

            return status, response_time, reason

        except httpx.ConnectTimeout:
            logger.warning(f"{address} timeout")
            return "DOWN", None, "timeout"

        except httpx.ConnectError:
            logger.warning(f"{address} dns_failure")
            return "DOWN", None, "dns_failure"

        except Exception as e:
            logger.error(f"{address} invalid_url {str(e)}")
            return "DOWN", None, "invalid_url"

    async def check_multiple_urls(self, urls):
        tasks = [self.check_single_url(url.address) for url in urls]
        return await asyncio.gather(*tasks)