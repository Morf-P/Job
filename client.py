import asyncio
import random

async def send_ping(writer):
    count = 0
    while True:
        await asyncio.sleep(random.uniform(0.3, 3))  # Случайный интервал от 300 до 3000 мс
        message = f"[PING] {count}"
        writer.write(message.encode())
        await writer.drain()
        count += 1

async def handle_response(reader):
    while True:
        data = await reader.readline()
        if not data:
            break
        message = data.decode().strip()
        print(f"Получено сообщение от сервера: {message}")

async def main():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    # Запуск клиента для отправки ping
    ping_task = asyncio.create_task(send_ping(writer))

    # Запуск клиента для обработки ответов
    response_task = asyncio.create_task(handle_response(reader))

    # Ожидание завершения обеих задач
    await ping_task
    await response_task

asyncio.run(main())
