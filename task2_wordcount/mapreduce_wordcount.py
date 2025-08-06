import requests
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import re


def fetch_text(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return ""


def clean_and_split(text: str) -> list[str]:
    # Залишаємо тільки слова, переводимо до нижнього регістру
    words = re.findall(r"\b\w+\b", text.lower())
    return words


def map_words(chunk: list[str]) -> Counter:
    return Counter(chunk)


def reduce_counters(counters: list[Counter]) -> Counter:
    total = Counter()
    for counter in counters:
        total.update(counter)
    return total


def visualize_top_words(counter: Counter, top_n: int = 10):
    top_items = counter.most_common(top_n)
    words, counts = zip(*top_items)

    plt.figure(figsize=(10, 5))
    plt.bar(words, counts)
    plt.xlabel("Слова")
    plt.ylabel("Кількість")
    plt.title(f"Топ {top_n} найвживаніших слів")
    plt.grid(axis="y")
    plt.tight_layout()

    plt.savefig("top_words.png")
    print("Графік збережено як top_words.png")



def main():
    url = input("Введи URL для аналізу тексту: ").strip()

    print("Завантаження тексту...")
    text = fetch_text(url)
    if not text:
        return

    words = clean_and_split(text)
    chunk_size = max(1, len(words) // 8)  # 8 потоків
    chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]

    print("Аналіз словами за допомогою MapReduce...")
    with ThreadPoolExecutor() as executor:
        counters = list(executor.map(map_words, chunks))

    total_counter = reduce_counters(counters)

    print("Візуалізація результатів...")
    visualize_top_words(total_counter)


if __name__ == "__main__":
    main()
