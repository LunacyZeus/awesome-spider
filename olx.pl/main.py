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
        url = f'olx.pl/dom-ogrod/meble/sofy-kanapy/q-sofa/?search%5Bfilter_enum_state%5D%5B0%5D=used&search%5Bfilter_enum_state%5D%5B1%5D=new&search%5Bprivate_business%5D=private'

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
