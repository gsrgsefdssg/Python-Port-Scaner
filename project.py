import tkinter as tk
from tkinter import scrolledtext
import socket
import asyncio

async def scaning(ip, port, log_widget):
    try:
        # Устанавливаем таймаут, чтобы не ждать вечно
        conn = asyncio.open_connection(ip, port)
        reader, writer = await asyncio.wait_for(conn, timeout=1.0)
        log_widget.insert(tk.END, f"✅ Порт {port} открыт\n")
        log_widget.see(tk.END)
        writer.close()
        await writer.wait_closed()
    except:
        pass

async def start_scan(entry, log_widget):
    domain = entry.get()
    log_widget.delete(1.0, tk.END)
    try:
        ip = socket.gethostbyname(domain)
        log_widget.insert(tk.END, f"Сканируем {domain} ({ip})...\n")
        
        tasks = [scaning(ip, i, log_widget) for i in range(1, 2000)]
        await asyncio.gather(*tasks)
        log_widget.insert(tk.END, "--- Сканирование завершено ---")
    except Exception as e:
        log_widget.insert(tk.END, f"Ошибка: {e}")

# Главная функция для запуска GUI вместе с asyncio
async def run_tk(root):
    while True:
        root.update() # Обновляем окно
        await asyncio.sleep(0.01) # Даем время на выполнение асинхронных задач

root = tk.Tk()
root.title("Async Port Scanner")

tk.Label(root, text="Введите домен:").pack()
entry = tk.Entry(root)
entry.pack()

btn = tk.Button(root, text="Сканировать", 
                command=lambda: asyncio.create_task(start_scan(entry, log)))
btn.pack()

log = scrolledtext.ScrolledText(root, width=40, height=15)
log.pack()

# Запуск
loop = asyncio.get_event_loop()
loop.run_until_complete(run_tk(root))
