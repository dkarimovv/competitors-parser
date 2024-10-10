# Competitor Data Scraper

This project is designed to scrape competitor data from a website using Playwright, process the data asynchronously, and export the results into CSV files. The project handles proxies, multiple workers, and asynchronous data gathering to ensure efficiency and scalability.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)

## Features

- **Asynchronous Data Scraping**: The scraper is built with `asyncio` and Playwright to fetch competitor data efficiently.
- **Proxy Management**: Rotating proxies are used to avoid being blocked, managed by the `ProxyManager`.
- **Multiple Workers**: The scraping process is split across multiple asynchronous workers to speed up data collection.
- **Data Export**: The collected data is exported into CSV files with options for saving the most recent or all available data.
- **File Health Check**: The system checks the existence of necessary files (`competitors.txt`, `config.txt`, `proxies.txt`) and creates them if they don't exist.

## Technologies

- **Python 3.10+**: The main programming language used for the project.
- **Playwright**: A browser automation library used for web scraping.
- **asyncio**: Used for managing asynchronous tasks, making the scraper efficient and capable of running multiple tasks concurrently.
- **aiohttp**: A library for making asynchronous HTTP requests, used for proxy checks.
- **pandas**: A data manipulation library used to create and export CSV files.
- **openpyxl**: A library for working with Excel files (optional, depending on CSV format requirements).

## File Setup
Make sure the following files exist in the root directory:

- **competitors.txt**: A file containing the competitors' IDs (one per line).
- **proxies.txt**: A list of proxies in the format ip:port:username:password.
- **config.txt**: Configuration file for scraper settings.

The system will automatically create these files if they are missing.


# RU
# Скрапер данных конкурентов

Этот проект предназначен для сбора данных о конкурентах с веб-сайта с помощью Playwright, обработки данных асинхронно и экспорта результатов в CSV-файлы. Проект использует прокси, несколько воркеров и асинхронное выполнение задач для повышения эффективности и масштабируемости.

## Оглавление

- [Особенности](#особенности)
- [Технологии](#технологии)


## Особенности

- **Асинхронный сбор данных**: Скрапер построен с использованием `asyncio` и Playwright для эффективного сбора данных о конкурентах.
- **Управление прокси**: Используются ротационные прокси для избежания блокировок, управление прокси выполняется через `ProxyManager`.
- **Множественные воркеры**: Процесс сбора данных разделён на несколько асинхронных воркеров для ускорения выполнения.
- **Экспорт данных**: Собранные данные экспортируются в CSV-файлы с возможностью сохранения только актуальных данных или всех доступных данных.
- **Проверка файлов**: Система проверяет наличие необходимых файлов (`competitors.txt`, `config.txt`, `proxies.txt`) и создаёт их, если они отсутствуют.

## Технологии

- **Python 3.10+**: Основной язык программирования, использованный в проекте.
- **Playwright**: Библиотека автоматизации браузера, используемая для сбора данных с веб-сайтов.
- **asyncio**: Используется для управления асинхронными задачами, что делает скрапер более эффективным и способным выполнять несколько задач одновременно.
- **aiohttp**: Библиотека для выполнения асинхронных HTTP-запросов, используется для проверки прокси.
- **pandas**: Библиотека для работы с данными, используемая для создания и экспорта CSV-файлов.
- **openpyxl**: Библиотека для работы с файлами Excel (опционально, в зависимости от требований к формату CSV).

## Установка

## Настройка файлов
Убедитесь, что в корневом каталоге существуют следующие файлы:

- **competitors.txt**: Файл, содержащий идентификаторы конкурентов (по одному на строку).
- **proxies.txt**: Список прокси в формате ip:port:username:password.
- **config.txt**: Файл конфигурации для настроек скрапера.
Система автоматически создаст эти файлы, если они отсутствуют.
