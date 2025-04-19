import os
from datetime import datetime, date
from typing import List, Dict

class Planner:
    def __init__(self, plans_dir: str = "data/days/"):
        self.plans_dir = plans_dir
        self.ensure_dirs()
        
    def ensure_dirs(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.plans_dir, exist_ok=True)
        
    def get_today_file(self) -> str:
        """Get path to today's plan file"""
        return os.path.join(self.plans_dir, f"{date.today()}.txt")
    
    def read_today(self) -> List[str]:
        """Read today's plans"""
        try:
            with open(self.get_today_file(), 'r', encoding='utf-8') as f:
                return f.readlines()
        except FileNotFoundError:
            return []

    def write_today(self, tasks: List[str]):
        """Write tasks to today's file"""
        with open(self.get_today_file(), 'w', encoding='utf-8') as f:
            f.writelines(tasks) 