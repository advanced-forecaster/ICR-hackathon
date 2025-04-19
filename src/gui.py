import tkinter as tk
from tkinter import ttk
import calendar
from datetime import date, datetime
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
            with open("data/schedule.txt", "r", encoding='utf-8') as f:
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
        self.current_date = datetime.today().strftime('%Y-%m-%d')  # You can set this as needed
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
        self.history.tag_configure('user', foreground='blue')
        self.history.tag_configure('assistant', foreground='green')
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
        tag = 'user' if from_user else 'assistant'
        self.history.insert('end', f"{prefix}{message}\n", tag)

        self.history.see('end')
        self.history.configure(state='disabled')
        
    def read_schedule(self):
        try:
            with open("data/schedule.txt", "r") as f:
                return f.read()
        except:
            return ""
            
    def read_daily_files(self):
        days_data = "data/days/"
        days_content = ""
        try:
            files = [f for f in os.listdir(days_data) if f.endswith(".txt")]
            files.sort() # Sort files alphabetically, which works for date-based filenames
            for date_filename in files:
                with open(os.path.join(days_data, date_filename), "r") as f:
                    date_str = date_filename.replace('.txt', '')
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    days_content += f"\n=== {date_obj.strftime('%A, %B %d, %Y')} ===\n"
                    days_diff = (datetime.today() - date_obj).days
                    if days_diff == 0:
                        days_content += " (Today)\n"
                    elif days_diff > 0:
                        days_content += f" ({days_diff} days ago)\n"
                    else:
                        days_content += f" (in {-days_diff} days)\n"
                    days_content += f.read()
        except:
            pass

        # print(days_content)
        return days_content


    def send_message(self):
        message = self.input.get().strip()
        if not message:
            return
            
        # Clear input first
        self.input.delete(0, 'end')
        
        # Add user message to display and history
        self.add_message(message, from_user=True)
        self.messages.append({'role': 'user', 'content': message})
        
        # Process in background
        async def process():
            context = {
                'current_date': self.current_date,
                'schedule': self.read_schedule(),
                'daily_plans': self.read_daily_files()
            }
            response = await self.llm.chat(messages=self.messages, context=context)
            
            # Add assistant response to display and history
            self.add_message(response, from_user=False)
            self.messages.append({'role': 'assistant', 'content': response})
            
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