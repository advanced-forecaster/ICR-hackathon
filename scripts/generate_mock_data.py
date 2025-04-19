import os
from datetime import datetime, timedelta
from pathlib import Path
import requests

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"

def get_llm_response(prompt):
    response = requests.post(OLLAMA_ENDPOINT, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"].strip()

def create_daily_entry(date):
    prompt = f"""Create a daily planner entry for a university student for {date.strftime('%Y-%m-%d')}. 
Include 2-3 classes/lectures, study tasks, assignments due, and maybe personal reminders.
Consider typical student activities like group projects, library study sessions, or club meetings.
Keep it simple and in plain text format without any special formatting, just plain text with newlines."""

    content = get_llm_response(prompt)
    
    # Ensure days directory exists
    days_dir = Path("days")
    days_dir.mkdir(exist_ok=True)
    
    # Write daily entry
    file_path = days_dir / f"{date.strftime('%Y-%m-%d')}.txt"
    with open(file_path, "w") as f:
        f.write(content)

def create_schedule():
    prompt = """Create a general weekly schedule for a university student.
Include regular classes, study blocks, club activities, and part-time work if any.
Consider typical student commitments like library hours, gym time, and social activities.
Keep it in plain text format with just days of the week and entries."""

    content = get_llm_response(prompt)
    
    # Write schedule
    with open("schedule.txt", "w") as f:
        f.write(content)

def main():
    # Generate entries for the next 7 days
    today = datetime.now()
    for i in range(7):
        date = today + timedelta(days=i)
        create_daily_entry(date)
        print(f"Created entry for {date.strftime('%Y-%m-%d')}")
    
    # Generate general schedule
    create_schedule()
    print("Created schedule.txt")

if __name__ == "__main__":
    main() 