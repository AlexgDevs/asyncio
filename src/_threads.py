from time import time
import threading
import requests

# ==================== CPU-bound ====================

def mult_two(n1: int, n2: int) -> int:
    return n1 * n2


print("=== CPU-bound задача (вычисления) ===")

start = time()
mult_two(2, 3)
mult_two(4, 5)
time_without = time() - start

th1 = threading.Thread(target=mult_two, args=(2, 3))
th2 = threading.Thread(target=mult_two, args=(4, 5))

start = time()
th1.start()
th2.start()
th1.join()
th2.join()
time_with = time() - start

print(f'Без потоков : {time_without:.6f} сек')
print(f'С потоками  : {time_with:.6f} сек')
print(f'Потоки медленнее в {time_with / time_without:.1f} раз\n')


# ==================== I/O-bound ====================

def fetch_url(url: str):
    response = requests.get(url, timeout=5)
    return response.status_code


print("=== I/O-bound задача (сеть) ===")

start = time()
fetch_url('https://www.google.com')
fetch_url('https://www.github.com')
time_without = time() - start

th1 = threading.Thread(target=fetch_url, args=('https://www.google.com',))
th2 = threading.Thread(target=fetch_url, args=('https://www.github.com',))

start = time()
th1.start()
th2.start()
th1.join()
th2.join()
time_with = time() - start

print(f'Без потоков : {time_without:.6f} сек')
print(f'С потоками  : {time_with:.6f} сек')
print(f'Потоки быстрее в {time_without / time_with:.1f} раз')


# ==================== Комментарии ====================
'''
Вывод:

CPU-bound (вычисления):
→ Многопоточность вредна. GIL не освобождается → overhead только замедляет.

I/O-bound (сеть, файлы, API):
→ Многопоточность полезна. Во время ожидания ответа GIL освобождается,
и потоки могут работать "параллельно".
'''
# 1.6