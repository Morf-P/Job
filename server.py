import asyncio
import time

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Новое соединение от {addr}")

    while True:
        data = await reader.readline()
        if not data:
            break

        message = data.decode().strip()
        print(f"Получил сообщение от {addr}: {message}")

        if message.startswith("[PING]"):
            response = f"[PONG] {message[6:]}"
        else:
            response = "[ОШИБКА] Неизвестное сообщение"

        writer.write(response.encode())
        await writer.drain()

        log_message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Request from {addr}: {message}; Response: {response}"
        print(log_message)
        with open("server.log", "a") as log_file:
            log_file.write(log_message + "\n")

    print(f"Соединение с {addr} прервано")

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    async with server:
        print("Сервер запущен. Прослушивание входящих соединений...")
        await server.serve_forever()

asyncio.run(main())
