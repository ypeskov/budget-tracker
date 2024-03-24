import requests
import concurrent.futures
import time
import threading


def send_request(stop_event):
    if stop_event.is_set():
        return None

    url = 'https://djangogramm-yd4vplntaq-uc.a.run.app/users/login/'
    data = {"email": "user1@example.com", "password": "qqq"}
    response = requests.get(url)
    # print(response)

    if response.status_code != 200:
        stop_event.set()

    return response.status_code


num_requests = 10000
max_workers = 200
stop_event = threading.Event()
start_time = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [executor.submit(send_request, stop_event) for _ in range(num_requests)]
    valid_requests = 0
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result is None:
            break
        if result == 200:
            valid_requests += 1
            print(f"Valid request {valid_requests}")

total_time = time.time() - start_time
requests_per_second = valid_requests / total_time if total_time > 0 else 0

print(f"Total time for {valid_requests} successful requests: {total_time} seconds")
print(f"Successful requests per second: {requests_per_second}")
