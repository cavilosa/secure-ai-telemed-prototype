from transformers import pipeline

print("Загружаю модель... Это может занять пару минут в первый раз.")

# Создаем пайплайн для генерации текста
# model="distilgpt2" - это легкая и быстрая модель
generator = pipeline("text-generation", model="distilgpt2")

input_text = "Security engineers are important because"

print(f"Запрос к ИИ: {input_text}")

# Генерируем ответ
response = generator(input_text, max_length=50, num_return_sequences=1)

print("\n--- Ответ ИИ ---")
print(response[0]['generated_text'])
print("----------------")