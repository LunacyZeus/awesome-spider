import asyncio
import re

import httpx
from DrissionPage._pages.chromium_page import ChromiumPage

from utils.csv_utils import write_csv_file
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
        #self.page.get(url=url)

        detail_list_xpath = '//div[contains(text(), "See ad details")]'
        detail_list_eles = self.page.s_eles(f"x:{detail_list_xpath}")

        data_list = []
        for ele in detail_list_eles:
            #parent = ele.parent(level_or_loc=6)
            #print([parent.text])

            #ele = detail_list_eles[0]
            ele_text = ele.parent(level_or_loc=6).text

            #print([ele_text])

            library_id = re.search(r'Library ID: (\d+)', ele_text)
            started_running = re.search(r'Started running on (.+)', ele_text)
            name = ele_text.split('\nSee ad details\n')[1].split('\n')[0]

            if library_id and started_running:

                #span_xpath = f'//span[contains(text(), "{name}")]'
                ele1 = ele.parent(level_or_loc=7)
                span_ele = ele1.s_eles(f"tag:a")
                href = ''
                for i in span_ele:
                    t_href = i.attr('href')
                    if 'https://www.facebook.com/' in t_href:
                        href = t_href

                print(f"Name: {name}")
                print(f"Href: {href}")
                print(f"Library ID: {library_id.group(1)}")
                print(f"Started running on: {started_running.group(1)}")
                data_list.append(
                    [
                        library_id.group(1),
                        started_running.group(1),
                        name,
                        href,
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                    ]
                )


            #input('-->')

        write_csv_file(keyword=keyword, data_list=data_list)


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
