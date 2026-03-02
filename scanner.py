import socket
import asyncio

async def scaning(ip, port):
    try:
        reader, writer = await asyncio.open_connection(ip, port) # Асинхронное TCP подключение

        print(f"Порт: {port} открыт")

        writer.close() # Закрывает соединение
        await writer.wait_closed()
    except: #Если будет ошибка то не выведет ее
        pass

async def main():
    domain = input("Введите домен для сканирования: ") # Пользователь вводит домен

    ip = socket.gethostbyname(domain) # Домен передается в переменную
    print(f"Сканируем {domain} ({ip})")
    
    tasks = []
    for i in range(2000):
        task = asyncio.create_task(scaning(ip, i))
        tasks.append(task)
    
    await asyncio.gather(*tasks) # Асинхронность 

asyncio.run(main())