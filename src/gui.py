import tkinter as tk
from tkinter import ttk
import calendar
from datetime import date
from ttkthemes import ThemedTk
from planner import Planner
from llm import LLMInterface
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os

class CalendarFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.today = date.today()
        self._create_widgets()
        
    def _create_widgets(self):
        # Month and year header
        header = ttk.Label(
            self, 
            text=f"{calendar.month_name[self.today.month]} {self.today.year}",
            font=('Arial', 10, 'bold')
        )
        header.pack(pady=5)
        
        # Calendar grid
        cal = calendar.monthcalendar(self.today.year, self.today.month)
        cal_frame = ttk.Frame(self)
        cal_frame.pack(fill='both', expand=True)
        
        # Weekday headers
        for i, day in enumerate("Mon Tue Wed Thu Fri Sat Sun".split()):
            ttk.Label(cal_frame, text=day).grid(row=0, column=i, padx=2)
            
        # Days
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day != 0:
                    style = 'CalCurrent.TLabel' if day == self.today.day else 'Cal.TLabel'
                    lbl = ttk.Label(cal_frame, text=str(day), style=style)
                    lbl.grid(row=week_num + 1, column=day_num, padx=2, pady=2)

class ScheduleFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.schedule = self._load_schedule()
        self._create_widgets()
        
    def _load_schedule(self):
        try:
            with open("schedule.txt", "r") as f:
                return f.read().strip().split("\n")
        except FileNotFoundError:
            return ["No schedule found"]
            
    def _create_widgets(self):
        ttk.Label(self, text="Weekly Schedule", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Create scrollable text widget
        text_widget = tk.Text(
            self,
            wrap='word',
            font=('Arial', 10),
            height=15,
            width=40
        )
        text_widget.pack(fill='both', expand=True, padx=5, pady=2)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=text_widget.yview)
        scrollbar.pack(side='right', fill='y')
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Insert schedule content
        for line in self.schedule:
            text_widget.insert('end', f"{line}\n")
            
        # Make text widget read-only
        text_widget.configure(state='disabled')

class ChatFrame(ttk.Frame):
    def __init__(self, parent, llm):
        super().__init__(parent)
        self.llm = llm
        self.current_date = "2025-04-20"  # You can set this as needed
        self.messages = []
        self._create_widgets()
        
    def _create_widgets(self):
        # Chat history
        self.history = tk.Text(
            self,
            wrap='word',
            state='disabled',
            font=('Arial', 10),
            height=20
        )
        self.history.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Input area
        input_frame = ttk.Frame(self)
        input_frame.pack(fill='x', padx=5, pady=5)
        
        self.input = ttk.Entry(input_frame)
        self.input.pack(side='left', fill='x', expand=True)
        
        send_btn = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_message
        )
        send_btn.pack(side='right', padx=5)
        
        # Bind Enter key
        self.input.bind('<Return>', lambda e: self.send_message())
        
    def add_message(self, message, from_user=True):
        self.history.configure(state='normal')
        prefix = "You: " if from_user else "Assistant: "
        self.history.insert('end', f"\n{prefix}{message}")
        self.history.see('end')
        self.history.configure(state='disabled')
        
    def read_schedule(self):
        try:
            with open("schedule.txt", "r") as f:
                return f.read()
        except:
            return ""
            
    def read_daily_files(self):
        days_content = ""
        try:
            for file in os.listdir("days"):
                if file.endswith(".txt"):
                    with open(os.path.join("days", file), "r") as f:
                        days_content += f"\n=== {file} ===\n"
                        days_content += f.read()
        except:
            pass
        return days_content
        
    def send_message(self):
        message = self.input.get().strip()
        if not message:
            return
            
        self.input.delete(0, 'end')
        self.add_message(message)
        
        # Show thinking message
        self.add_message("Thinking...", from_user=False)
        
        # Process in background
        async def process():
            # Build context from schedule and daily files
            context = f"""Current date: {self.current_date}

Schedule:
{self.read_schedule()}

Daily plans:
{self.read_daily_files()}

User question: {message}

Based on the schedule and daily plans above, please help the user."""

            response = await self.llm.chat(context)
            
            # Remove thinking message
            self.history.configure(state='normal')
            self.history.delete("end-2c linestart", "end")
            self.history.configure(state='disabled')
            
            self.add_message(response, from_user=False)
            
        asyncio.run(process())

class PlannerGUI:
    def __init__(self):
        self.planner = Planner()
        self.llm = LLMInterface()
        
        # Create themed window
        self.root = ThemedTk(theme="arc")  # Modern theme
        self.root.title("AI Planner")
        self.root.geometry("1000x600")
        
        # Configure styles
        style = ttk.Style()
        style.configure('CalCurrent.TLabel', foreground='blue', font=('Arial', 10, 'bold'))
        style.configure('Cal.TLabel', font=('Arial', 10))
        
        self._create_widgets()
        
    def _create_widgets(self):
        # Main container
        main = ttk.PanedWindow(self.root, orient='horizontal')
        main.pack(fill='both', expand=True)
        
        # Left panel (Calendar + Schedule)
        left_panel = ttk.Frame(main)
        main.add(left_panel, weight=1)
        
        # Calendar
        cal = CalendarFrame(left_panel)
        cal.pack(fill='x', padx=10, pady=10)
        
        ttk.Separator(left_panel, orient='horizontal').pack(fill='x', padx=10, pady=10)
        
        # Schedule
        schedules = ScheduleFrame(left_panel)
        schedules.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Right panel (Chat)
        chat = ChatFrame(main, self.llm)
        main.add(chat, weight=2)
        
    def run(self):
        self.root.mainloop()

def main():
    print("Starting application...")
    # Initialize and run GUI
    app = PlannerGUI()
    print("Created GUI...")
    app.run()
    print("Running main loop...")

if __name__ == "__main__":
    main() 