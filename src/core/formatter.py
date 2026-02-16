import pandas as pd
from datetime import datetime

def format_program_doc(row: pd.Series) -> str:
    """Formats a single program row into a text document."""
    # Logic from generate_knowledge_corpus_txt.py
    year_raw = str(row["year"]) if pd.notna(row["year"]) else "Не указан"
    year_parts = [part.strip() for part in year_raw.split(",") if part.strip().isdigit() and len(part.strip()) <= 2]
    year_clean = ", ".join(year_parts) if year_parts else "Не указан"

    text = f"""Программа: {row.get('name_prog', '')}
    Уровень: {row.get('level', '')}
    Курс: {year_clean}
    Тип: {row.get('type', '')}
    Язык: {row.get('language', '')}
    Длительность: {row.get('duration', '')}
    Старт программы: {row.get('start', '')}
    Дедлайн подачи: {row.get('deadline', '')}
    Требования: {row.get('requirements', '') if pd.notna(row.get('requirements')) else 'Не указаны'}
    Количество мест: {row.get('quantity', '')}
    Финансирование: {row.get('financing', '') if pd.notna(row.get('financing')) else 'Не указано'}
    Проживание: {row.get('accommodation', '')}
    Описание программы: {row.get('description_prog', '') if pd.notna(row.get('description_prog')) else 'Нет описания'}

    ВУЗ: {row.get('name_univ', '')} ({row.get('short_name', '')})
    Город: {row.get('city', '')}, {row.get('region', '')}
    Рейтинг: {row.get('rating', '')}
    Описание вуза: {row.get('description_univ', '') if pd.notna(row.get('description_univ')) else 'Нет описания'}
    Сайт: {row.get('website', '')}
    Контактное лицо: {row.get('contact_person_name', '')}, {row.get('contact_person_email', '')}, {row.get('contact_person_phone', '')}"""
    return text.strip()

def generate_universities_section_md(df: pd.DataFrame) -> str:
    """Generates Markdown section for universities."""
    lines = []
    lines.append("## Университеты\n")
    lines.append(f"*Всего записей: {len(df)}*\n")
    lines.append("---\n")
    
    for idx, row in df.iterrows():
        # Heuristic to find name column
        name_col = next((col for col in df.columns if 'name' in col.lower() or 'название' in col.lower() or 'университет' in col.lower()), df.columns[0])
        uni_name = row.get(name_col, f"Университет {idx + 1}")
        
        lines.append(f"### {uni_name}\n")
        
        for col_name in df.columns:
            if col_name != name_col:
                value = row.get(col_name)
                if pd.notna(value) and str(value).strip():
                    lines.append(f"- **{col_name}**: {value}")
        
        lines.append("\n---\n")
    
    return "\n".join(lines)

def generate_programs_section_md(df: pd.DataFrame) -> str:
    """Generates Markdown section for programs."""
    lines = []
    lines.append("## Образовательные программы\n")
    lines.append(f"*Всего записей: {len(df)}*\n")
    lines.append("---\n")
    
    for idx, row in df.iterrows():
        # Heuristic to find name column
        name_col = next((col for col in df.columns if 'name' in col.lower() or 'название' in col.lower() or 'программ' in col.lower()), df.columns[0])
        prog_name = row.get(name_col, f"Программа {idx + 1}")
        
        lines.append(f"### {prog_name}\n")
        
        for col_name in df.columns:
            if col_name != name_col:
                value = row.get(col_name)
                if pd.notna(value) and str(value).strip():
                    lines.append(f"- **{col_name}**: {value}")
        
        lines.append("\n---\n")
    
    return "\n".join(lines)

def generate_metadata_section_md() -> str:
    lines = []
    lines.append("---\n")
    lines.append("## Метаданные\n")
    lines.append(f"- **Дата генерации**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("- **Формат**: Markdown (оптимизировано для RAG)")
    lines.append("- **Структура**: Университеты + Образовательные программы")
    lines.append("---\n")
    return "\n".join(lines)
