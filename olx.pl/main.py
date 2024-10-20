import asyncio

import httpx
from DrissionPage._pages.chromium_page import ChromiumPage

from utils.dp import get_page


class MainProcess(object):
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.page: ChromiumPage = None

    async def start_dp(self):
        debugger_port = 12345
        self.page = get_page(debugger_port=debugger_port)

    async def handle(self):
        keyword = 'Salwar'
        url = f'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BD&media_type=all&q={keyword}&search_type=keyword_unordered&source=ad-report'

        a_xpath = '//div[@data-cy="l-card" and @data-testid="l-card"]'
        eles = self.page.s_eles(f"x:{a_xpath}")
        for ele in eles:
            b_xpath = '//div[@data-cy="ad-card-title"]'
            card_title_ele = ele.ele(f'x:{b_xpath}')
            text = card_title_ele.text
            tmp = text.split("\n")
            product_name = tmp[0]
            price = tmp[1]
            a_ele = card_title_ele.ele(f"tag:a")
            href = a_ele.attr('href')
            print(f"name({product_name}) price({price}) href({href})")

    async def run(self):
        await self.start_dp()  # 启动dp框架
        await self.handle()


async def main():
    process = MainProcess()
    await process.run()


def test():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


if __name__ == '__main__':
    test()
