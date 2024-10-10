import asyncio
import aiohttp
from playwright.async_api import async_playwright

class ProxyManager:
    def __init__(self, file_path='proxies.txt'):
        self.file_path = file_path
        self.lock = asyncio.Lock()  # Блокировка для синхронизации доступа к прокси
        self.proxies = self.load_proxies()  # Загружаем прокси при инициализации

    def load_proxies(self):
        with open(self.file_path, "r") as f:
            lines = f.readlines()
            return [line.strip().replace("*", "").strip() for line in lines]

    async def check_proxy(self, proxy):
        """ Проверяем работоспособность прокси через подключение к Google """
        proxy_url = f"http://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}"  # Формат для HTTP-прокси
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://google.com', proxy=proxy_url, timeout=10):
                    print(f"Прокси {proxy_url} работает.")
                    return True
        except:
            print(f"Прокси {proxy_url} не работает.")
            return False

    async def get_proxy(self):
        """ Синхронный доступ к прокси, чтобы воркеры не использовали одну и ту же прокси. """
        async with self.lock:  # Добавляем блокировку
            while self.proxies:
                proxy = self.proxies.pop(0)  # Берем первую прокси из списка
                proxy_details = proxy.split(':')

                # Проверяем, работает ли прокси
                if await self.check_proxy(proxy_details):
                    self.proxies.append(proxy)  # Возвращаем прокси в конец списка для повторного использования
                    return proxy_details
                else:
                    print(f"Прокси {proxy} исключена из списка.")
                    continue

            raise Exception("Нет доступных прокси.")

async def scrape_page(page):
    all_data = []
    cards = await page.query_selector_all("div.col-12.col-lg-5, div.col-12.col-lg-7")

    for i in range(0, len(cards), 2):
        data1 = [await dd.competitorser_text() for dd in await cards[i].query_selector_all('dd')]
        data2 = [await dd.competitorser_text() for dd in await cards[i+1].query_selector_all('dd')]
        all_data.append(data1 + data2)

    return all_data

async def get_data_from_web(competitors: str, worker_id: int, proxy_manager: ProxyManager):
    proxy = await proxy_manager.get_proxy()  # Асинхронно получаем рабочую прокси
    link = 'https://link-to-shop.com/'

    print(f"[Worker-{worker_id}] Использует прокси: {proxy[0]}:{proxy[1]}")  # Выводим информацию о прокси

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, proxy={
            'server': f'http://{proxy[0]}:{proxy[1]}',  # Используем HTTP
            'username': proxy[2],
            'password': proxy[3],
        })
        page = await browser.new_page()

        await page.goto(link)
        await asyncio.sleep(10)
        print(f'[Worker-{worker_id}] Зашли на сайт')

        await page.click('#frmQuickSearch > div.d-none.d-lg-block > div > label:nth-child(16)')
        await page.fill('#ogrnUlDoc', competitors)
        await page.click('#frmQuickSearch > div.d-flex.flex-nowrap.flex-column.flex-lg-row > div.d-flex.flex-column.align-items-stretch.mt-2.mt-lg-0.ml-lg-2.flex-sm-row.align-items-sm-start > button')

        print(f'[Worker-{worker_id}] Поиск по Конкурента {competitors}')
        # await page.wait_for_load_state('networkidle')
        await asyncio.sleep(10)

        cards = await page.query_selector_all("div.col-12.col-lg-5, div.col-12.col-lg-7")
        if not cards:
            print(f'[Worker-{worker_id}] Нет данных для Конкурента {competitors}, записываем в файл.')
            with open('nodata_companies.txt', 'a', encoding='utf-8') as file:
                file.write(f'{competitors}\n')
            await browser.close()
            return []

        all_scraped_data = []

        print(f'[Worker-{worker_id}] Собираем данные со страницы')
        while True:
            page_data = await scrape_page(page)
            all_scraped_data.extend(page_data)

            next_button = await page.query_selector("text=Следующая")
            if next_button is None:
                break  # Если кнопка "Следующая" не найдена, выходим из цикла

            await next_button.click()
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(3)

        print(f'[Worker-{worker_id}] Данные успешно собрались')
        await browser.close()
        return all_scraped_data

def get_competitorss() -> list:
    """ Функция для чтения Конкурента из файла 'competitors.txt' """
    with open('competitors.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()  # Чтение всех строк в список
        lines = [line.strip() for line in lines]  # Удаление лишних пробелов и символов перевода строки
    return lines
