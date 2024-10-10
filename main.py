import os
import asyncio
from parser import get_data_from_web, get_competitorss, ProxyManager
from xlsx import create_csv

def check_health():
    competitors_file = False
    config_file = False
    proxy_file = False
    if os.path.exists('competitors.txt'):
        competitors_file = True
    else:
        print(f"Файл competitors.txt не найден.")
        print(f'Создаем файл competitors.txt')
        my_file = open("competitors.txt", "w+")
        my_file.close()
        if os.path.exists('competitors.txt'):
            print('Файл был успешно создан')
        else:
            print('Возникла неизвестная ошибка')

    # Заглушка под конфиг. Для наглядность использую txt файл
    if os.path.exists('config.txt'):
        config_file = True
    else:
        print(f"Файл config.txt не найден.")
        print(f'Создаем файл config.txt')
        my_file = open("config.txt", "w+")
        my_file.write('TEST_1=TRUE\n')
        my_file.write('TEST_2=TRUE')
        my_file.close()
        if os.path.exists('config.txt'):
            print('Файл был успешно создан \n Выберите настройки в config.txt')
        else:
            print('Возникла неизвестная ошибка')
    if os.path.exists('proxies.txt'):
        proxy_file = True
    else:
        print(f"Файл proxies.txt не найден.")
        print(f'Создаем файл proxies.txt')
        my_file = open("proxies.txt", "w+")
        my_file.close()
        if os.path.exists('proxies.txt'):
            print('Файл был успешно создан')
        else:
            print('Возникла неизвестная ошибка')
    
    return competitors_file, config_file, proxy_file

async def worker(competitors_queue, results, worker_id, proxy_manager):
    while not competitors_queue.empty():
        competitors = await competitors_queue.get()  # Забираем Конкурентов из очереди
        print(f"[Worker-{worker_id}] Начинаем обработку Конкурентов: {competitors}")
        try:
            # Добавляем тайм-аут на выполнение задачи
            data = await asyncio.wait_for(get_data_from_web(competitors, worker_id, proxy_manager), timeout=60)
            results.append((competitors, data))  # Добавляем результат в общий список
            print(f"[Worker-{worker_id}] Обработка Конкурента {competitors} завершена")
        except asyncio.TimeoutError:
            print(f"[Worker-{worker_id}] Задача с Конкурентом {competitors} превысила время ожидания и была пропущена.")

        except Exception as e:
            print(f"[Worker-{worker_id}] Ошибка при обработке Конкурента {competitors}: {e}")
        competitors_queue.task_done()

async def run(competitorss, num_workers=3):
    competitors_queue = asyncio.Queue()
    results = []

    # Инициализируем ProxyManager
    proxy_manager = ProxyManager('proxies.txt')

    for competitors in competitorss:
        await competitors_queue.put(competitors)

    tasks = [asyncio.create_task(worker(competitors_queue, results, i+1, proxy_manager)) for i in range(num_workers)]
    await asyncio.gather(*tasks)
    await competitors_queue.join()

    print(f"Все задачи завершены. Обработано {len(results)} Конкурентов.")
    return results

if __name__ == '__main__':
    # Проверяем наличие необходимых файлов
    competitors_file, config_file, proxy_file = check_health()
    if not all([competitors_file, config_file, proxy_file]):
        print("Не все необходимые файлы найдены. Проверьте файлы и повторите попытку.")
        quit()

    competitorss = get_competitorss()
    if not competitorss:
        print('Заполните файл competitors.txt')
        quit()

    # Асинхронный запуск обработки с 5 процессами и тайм-аутами
    print(f"Начало обработки {len(competitorss)} Конкурентов с {5} рабочими процессами...")
    data = asyncio.run(run(competitorss, num_workers=5))

    # Создание Excel файла на основе всех данных
    create_csv([competitors for competitors, _ in data], [result for _, result in data], 'actual')
    print(f"Создан файл с результатами для {len(data)} Конкурентов.")
