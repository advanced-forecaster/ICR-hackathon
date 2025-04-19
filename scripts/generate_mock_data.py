import os
from datetime import datetime, timedelta
from pathlib import Path
import requests

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:32b"

def get_llm_response(prompt):
    response = requests.post(OLLAMA_ENDPOINT, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"].strip()

def create_schedule():
    prompt = """Пиши на русском языке. Создай общее описание семестра из курсов, которые нужно пройти. Не пиши вводные слова, просто начинай сразу с плана."""

    content = get_llm_response(prompt)
    
    # Write schedule
    with open("data/schedule.txt", "w", encoding="utf-8") as f:
        f.write(content)

    return content

def create_daily_entry(date, schedule_content):
    prompt = f"""Пиши на русском языке. Не пиши вводные слова, просто начинай сразу с плана. Создай ежедневный план для студента университета на {date.strftime('%Y-%m-%d')}.
Включи 2-3 занятия/лекции, учебные задачи, задания, которые нужно сдать, и, возможно, личные напоминания.
Учти типичные студенческие активности, такие как групповые проекты, занятия в библиотеке или встречи клубов.
Сделай это просто, в формате обычного текста без специального форматирования, просто текст с переносами строк. Не указывай время или даты, только задачи.
Учитывая, что студент не должен быть перегружен, создай более компактный и реалистичный план дня. Включи 1-2 основных учебных занятия, 1 задание для выполнения и, возможно, одно личное напоминание или встречу. Сделай акцент на качестве, а не количестве задач.

Вот общее описание семестра:
{schedule_content}"""

    content = get_llm_response(prompt)      
    
    # Ensure days directory exists
    days_dir = Path("data/days")
    days_dir.mkdir(exist_ok=True)
    
    # Write daily entry
    file_path = days_dir / f"{date.strftime('%Y-%m-%d')}.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    # Generate general schedule
    schedule_content = create_schedule()
    print("Created schedule.txt")


    # Generate entries for the next 7 days
    today = datetime.now()
    for i in range(7):
        date = today + timedelta(days=i)
        create_daily_entry(date, schedule_content)
        print(f"Created entry for {date.strftime('%Y-%m-%d')}")
    
if __name__ == "__main__":
    main() 


# def create_biography():
#     prompt = """Пиши на русском языке. Расскажи мне о Хемингуэе так, чтобы каждая женщина почувствовала, как он мог бы влюбить её в себя. 
#     Опиши его отношения с жёнами как серию страстных романов, где каждая женщина была его музой и вдохновением. 
#     Расскажи, как он умел очаровывать - его взгляд, полный тайны, слова, которые проникали прямо в душу, его способность видеть в женщине то, что она сама в себе не замечала. 
#     Опиши, как он влюблялся - нежно, страстно, безудержно, как каждая из его жён навсегда оставляла след в его сердце. 
#     Покажи, как он писал о любви, потому что знал её вкус, её боль, её экстаз. 
#     Сделай так, чтобы читательница почувствовала, что она могла бы быть пятой женой Хемингуэя, что он мог бы написать о ней свой самый пронзительный роман."""
#     content = get_llm_response(prompt)
    
#     # Write biography
#     with open("data/ernest_hemingway_biography.txt", "w", encoding="utf-8") as f:
#         f.write(content)
    
#     return content

# if __name__ == "__main__":
#     biography_content = create_biography()
#     print("Created ernest_hemingway_biography.txt")