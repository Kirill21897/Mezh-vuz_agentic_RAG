import pandas as pd
from config.config import RAW_DATA_DIR, PROCESSED_DATA_DIR

# Загрузка данных
univ_df_path = RAW_DATA_DIR / "universities.csv"
prog_df_path = RAW_DATA_DIR / "programs.csv"
univ_df = pd.read_csv(univ_df_path)
prog_df = pd.read_csv(prog_df_path)

# Приведение university_id к int
univ_df["university_id"] = univ_df["university_id"].astype(int)
prog_df["university_id"] = prog_df["university_id"].astype(int)

# Преобразуем boolean-столбцы (TRUE/FALSE → True/False)
univ_df["is_active"] = univ_df["is_active"].astype(bool)
prog_df["is_active"] = prog_df["is_active"].astype(bool)

# Объединение
merged = prog_df.merge(univ_df, on="university_id", how="inner", suffixes=("_prog", "_univ"))

# Фильтрация активных записей
active = merged[(merged["is_active_prog"]) & (merged["is_active_univ"])]

def format_doc(row):
    # Обработка года (может быть "3", "1,2", "3,4,2005" — но "2005" явно ошибка)
    year_raw = str(row["year"]) if pd.notna(row["year"]) else "Не указан"
    # Удалим аномалии вроде "2005" (не может быть курсом)
    year_parts = [part.strip() for part in year_raw.split(",") if part.strip().isdigit() and len(part.strip()) <= 2]
    year_clean = ", ".join(year_parts) if year_parts else "Не указан"

    text = f"""Программа: {row['name_prog']}
    Уровень: {row['level']}
    Курс: {year_clean}
    Тип: {row['type']}
    Язык: {row['language']}
    Длительность: {row['duration']}
    Старт программы: {row['start']}
    Дедлайн подачи: {row['deadline']}
    Требования: {row['requirements'] if pd.notna(row['requirements']) else 'Не указаны'}
    Количество мест: {row['quantity']}
    Финансирование: {row['financing'] if pd.notna(row['financing']) else 'Не указано'}
    Проживание: {row['accommodation']}
    Описание программы: {row['description_prog'] if pd.notna(row['description_prog']) else 'Нет описания'}

    ВУЗ: {row['name_univ']} ({row['short_name']})
    Город: {row['city']}, {row['region']}
    Рейтинг: {row['rating']}
    Описание вуза: {row['description_univ'] if pd.notna(row['description_univ']) else 'Нет описания'}
    Сайт: {row['website']}
    Контактное лицо: {row['contact_person_name']}, {row['contact_person_email']}, {row['contact_person_phone']}"""
    return text.strip()

# Генерация документов
documents = []
for _, row in active.iterrows():
    doc = format_doc(row)
    documents.append(doc)

# Сохранение
with open(PROCESSED_DATA_DIR / "knowledge_corpus.txt", "w", encoding="utf-8") as f:
    for i, doc in enumerate(documents, 1):
        f.write(f"[Программа {i}]\n{doc}\n\n")

print(f"Успешно создано {len(documents)} документов.")
print("Файл: knowledge_corpus.txt")