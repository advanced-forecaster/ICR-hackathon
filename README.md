# Personal LLM-Powered Planner

## Description

This repository contains a personal planning application built with a graphical user interface (GUI) and integrated with a local Large Language Model (LLM). The application allows users to manage daily plans, view a weekly schedule, and interact with an LLM for planning assistance.

## Features

*   **GUI:** User-friendly interface for interacting with the planner.
*   **Daily Planning:** Edit and save plans for individual days.
*   **Weekly Schedule:** Display a predefined weekly schedule.
*   **LLM Integration:** Chat with a local LLM to get help with planning and task management.

## Technologies Used

*   Python
*   Tkinter (for GUI)
*   Ollama (for local LLM interaction)
*   `requirements.txt` lists other dependencies like `torch`, `transformers`, `sentence-transformers`, etc.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up Ollama:**
    *   Download and install Ollama from [ollama.ai](https://ollama.ai/).
    *   Pull the required LLM model (e.g., `qwen2.5:7b` as seen in `src/llm.py`). You can do this by running:
        ```bash
        ollama pull qwen2.5:7b
        ```

## Usage

1.  **Run the application:**
    ```bash
    python src/gui.py
    ```
2.  **GUI Interaction:**
    *   Use the calendar to select a day and edit its plan.
    *   View the weekly schedule.
    *   Interact with the LLM through the chat interface.

## Project Structure

*   `src/`: Contains the main application source code (`gui.py`, `llm.py`, `planner.py`).
*   `data/`: Stores application data, such as daily plans and the weekly schedule.
*   `notebooks/`: Contains Jupyter notebooks, potentially for LLM prompting experiments.
*   `scripts/`: May contain utility scripts.
*   `requirements.txt`: Lists Python dependencies.

## Contributing

(Add information on how to contribute if applicable.)

## License

(Add license information if applicable.)