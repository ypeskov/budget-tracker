import requests
import concurrent.futures
import time
import threading

# Функция для отправки запроса
def send_request(stop_event):
    if stop_event.is_set():
        return None

    url = 'https://budgeter-api.peskov.info/auth/login/'
    data = {"email": "user1@example.com", "password": "qqq"}
    response = requests.post(url, json=data)

    if response.status_code != 200:
        stop_event.set()

    return response.status_code

# Количество запросов
num_requests = 200

# Количество параллельных запросов
max_workers = 200

# Событие для остановки выполнения
stop_event = threading.Event()

# Засекаем время начала выполнения
start_time = time.time()

# Использование ThreadPoolExecutor для параллельной отправки запросов
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [executor.submit(send_request, stop_event) for _ in range(num_requests)]
    valid_requests = 0
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result is None:
            break
        if result == 200:
            valid_requests += 1

# Вычисляем общее время выполнения и количество успешных запросов в секунду
total_time = time.time() - start_time
requests_per_second = valid_requests / total_time if total_time > 0 else 0

print(f"Total time for {valid_requests} successful requests: {total_time} seconds")
print(f"Successful requests per second: {requests_per_second}")
