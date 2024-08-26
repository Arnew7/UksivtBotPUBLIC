import gc
from bs4 import BeautifulSoup
import asyncio
from PyPDF2 import PdfReader
import datetime
import aiohttp
offset = datetime.timedelta(hours=5)
tz = datetime.timezone(offset)

async def TGstart():
    def Date():

        Day = datetime.date.today().strftime('%d')
        Month = datetime.date.today().strftime('%m')
        today = datetime.date.today()
        tomorrow_d = today + datetime.timedelta(days=1)
        Day_t = tomorrow_d.strftime('%d')
        Month_t = tomorrow_d.strftime('%m')
        return Day, Month, Day_t, Month_t, today

    Day, Month, Day_t, Month_t, today = Date()


    async def start():
        today = await body(Day, Month)
        tomorrow_d = await body(Day_t, Month_t)
        result = f"Замены: на {today}"
        resultT = f"Замены: на {tomorrow_d}"
        return result, resultT

    async def body(Day, Month):
        async def search_link_async(arr_link, date):
            tasks = [asyncio.create_task(find_link_async(i, date)) for i in arr_link]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result is not None:
                    return f"https://www.uksivt.ru/zameny{result[8:].replace(' ', '%20')}"
            return "Ссылки не найдено"

        async def find_link_async(link, date):
            if find_substring(link, date):
                return link

        async def scrap_page_async(url):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    arr = [link.get('href') for link in soup.find_all('a')]
                    del arr[400:]
                    del arr[:330]

            return arr

        def find_substring(string, substring):
            return substring in string if string else False

        async def main():
            url = 'https://www.uksivt.ru/zameny'
            date = f"{Day}.{Month}"
            print(date)
            arr_links = await scrap_page_async(url)
            result = await search_link_async(arr_links, date)
            result = result.replace("/zameny", "")
            return result

        async def download_pdf(url):
            if url == 'Ссылки не найдено':
                return f"Ссылки не найдено"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        with open("file.pdf", "wb") as file:
                            file.write(await response.read())
                        reader = PdfReader("file.pdf")
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text()
                        return text
                    else:
                        print(f"File not found at {url}")

        url = await main()

        if url == 'Ссылки не найдено':
            return f"Ссылки не найдено"
        if url.endswith(".docx"):
            return ("Файл типа docx, не могу открыть")
        text = await download_pdf(url)
        text = text.upper()



        text = (text.replace("24уКСК -2", "24уКСК-2").replace("24уКСК -1", "24уКСК-1")
        .replace("24СА -1", "24СА-1").replace("24СА -2", "24СА-2").replace("24СА -3", "24СА-3").replace("24П -1", "24П-1")
        .replace("24П -2", "24П-2").replace("24П -3", "24П-3").replace("24П -4", "24П-4").replace("24П -5", "24П-5")
        .replace("24ВЕБ -1", "24ВЕБ-1").replace("24ВЕБ -2", "24ВЕБ-2").replace("24ИИС -1", "24ИИС-1")
        .replace("24ИИС -2", "24ИИС-2").replace("24ОИБ -1", "24ОИБ-1")
        .replace("24ОИБ -2", "24ОИБ-2").replace("24ОИБ -3", "24ОИБ-3").replace("24з -1", "24з-1")
        .replace("24з -2", "24з-2").replace("24Э -1", "24Э-1").replace("24Э -2", "24Э-2").replace("24Ю -1", "24Ю-1")
        .replace("24Ю -2", "24Ю-2").replace("24Ю -3", "24Ю-3")
        .replace("24Ю -4", "24Ю-4").replace("24ПД -1", "24ПД-1").replace("24ПД -2", "24ПД-2")
        .replace("24ПД -3", "24ПД-3").replace("24Л -1", "24Л-1").replace("24Л -2", "24Л-2")
        .replace("24уЛ -1", "24уЛ-1").replace("23ПО -2", "23ПО-2")
        .replace('23ВЕБ -1', '23ВЕБ-1').replace('23ВЕБ -2','23ВЕБ-2')
        .replace('23З -1','23З-1').replace('23З -2', '23З-2').replace('23Л -1','23Л-1').replace('23Л -2', '23Л-2')
        .replace('23ОИБ -1', '23ОИБ-1')
        .replace('23ОИБ -2','23ОИБ-2').replace('23П -1', '23П-1').replace('23П -2', '23П-2').replace('23П -3',
        '23П-3').replace('23П -4','23П-4').replace('23П -5', '23П-5').replace('23П -6',
        '23П-6').replace('23ПД -1', '23ПД-1').replace('23ПД -2', '23ПД-2').replace('23ПО -1',
                                                                                                                  '23ПО-1').replace(
            '23ПО -2', '23ПО-2').replace('23ПО -3', '23ПО-3').replace('23ПО -4',
                                                                      '23ПО-4').replace('23ПО -5', '23ПО-5').replace(
            '23СА -1', '23СА-1').replace('23СА -2',
                                         '23СА-2').replace('23СА -3', '23СА-3').replace('23уКСК -1', '23уКСК-1').replace(
            '23уЛ -1',
            '23уЛ-1').replace('23Э -1', '23Э-1').replace('23Э -2', '23Э-2').replace('22БД -1',
                                                                                    '22БД-1').replace('22ВЕБ -1',
                                                                                                      '22ВЕБ-1').replace(
            '22ВЕБ -2', '22ВЕБ-2').replace('22ЗИО -1',
                                           '22ЗИО-1').replace('22ЗИО -2', '22ЗИО-2').replace('22ИС -1', '22ИС-1').replace(
            '22Л -1',
            '22Л-1').replace('22Л -2', '22Л-2').replace('22ОИБ -1', '22ОИБ-1').replace('22ОИБ -2',
                                                                                       '22ОИБ-2').replace('22П -1',
                                                                                                          '22П-1').replace(
            '22П -2', '22П-2').replace('22П -3',
                                       '22П-3').replace('22ПД -1', '22ПД-1').replace('22ПД -2',
                                                                                     '22ПД-2').replace('22ПО -1',
                                                                                                       '22ПО-1').replace(
            '22ПО -2', '22ПО-2').replace('22ПО -3',
                                         '22ПО-3').replace('22ПСА -1',
                                                           '22ПСА-1').replace('22ПСА -2', '22ПСА-2').replace('22ПСА -3',
                                                                                                             '22ПСА-3').replace(
            '22уКСК -1',
            '22уКСК-1').replace('22уЛ -1', '22уЛ-1').replace('22Э -1', '22Э-1').replace('21БД - 1',
                                                                                        '21БД-1').replace('21ВЕБ -1',
                                                                                                          '21ВЕБ-1').replace(
            '21ВЕБ -2', '21ВЕБ-2').replace('21ЗИО -1',
                                           '21ЗИО-1').replace('21ЗИО -2', '21ЗИО-2').replace('21ЗИО -3', '21ЗИО-3').replace(
            '21ИС -1',
            '21ИС-1').replace('21Л -1', '21Л-1').replace('21Л -2', '21Л-2').replace('21ОИБ -1',
                                                                                    '21ОИБ-1').replace('21ОИБ -2',
                                                                                                       '21ОИБ-2').replace(
            '21ОИБ -3', '21ОИБ-3').replace('21П -1',
                                           '21П-1').replace('21П -2', '21П-2').replace('21П -3', '21П-3').replace('21ПД -1',
                                                                                                                  '21ПД-1').replace(
            '21ПД -2', '21ПД-2').replace('21ПД -3', '21ПД-3').replace('21ПО -1',
                                                                      '21ПО-1').replace('21ПО -2', '21ПО-2').replace(
            '21ПО -3', '21ПО-3').replace('21ПО -4',
                                         '21ПО-4').replace('21ПСА -1', '21ПСА-1').replace('21ПСА -2', '21ПСА-2').replace(
            '21ПСА -3',
            '21ПСА-3').replace('21ПСА -4', '21ПСА-4').replace('21ПСА -5',
                                                              '21ПСА-5').replace('21ПСА -6', '21ПСА-6').replace('21СА -1',
                                                                                                                '21СА-1').replace(
            '21СА -2',
            '21СА-2').replace('21уКСК -1', '21уКСК-1'))

        return text
        # Функция для удаления лишних символов из текста
    text, textT = await start()

    return text, textT

text, textT = asyncio.run(TGstart())
gc.collect()



