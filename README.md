# DroneSwarm Logic Core - Offline Dataset Generator

An autonomous drone task decomposition engine powered by **DeepSeek-Coder-V2** via **Ollama**. This tool transforms high-level building inspection tasks into mid-level technical subtasks with precise GPS coordinate mapping.

## 🚀 Features
- **Local AI Processing:** Runs 100% offline using Ollama.
- **Recursive Decomposition:** Breaks complex tasks into 3-5 logical subtasks.
- **Geometry Mapping:** Automatically maps building features (Wall AB, Corner C, etc.) to coordinate tags.
- **Thinking Process:** Captures AI reasoning steps for every decision.

## 🛠️ Setup
1. Install [Ollama](https://ollama.com/).
2. Pull the model: `ollama run deepseek-coder-v2:16b-lite-instruct-q4_K_M`
3. Install requirements: `pip install requests`
4. Run the generator: `python main.py`

## 🤖 Workflow Automation
This project includes an automation suite designed to bridge the gap between web data and structured storage:
- **Browser-to-Sheet Pipeline:** Automated extraction of building data from web interfaces.
- **Python Integration:** Seamlessly passes raw web data into the DeepSeek Logic Core.
- **Google Sheets API:** Automatically updates the final dataset into cloud storage for team collaboration.

## 📊 Sample Output
The tool generates a structured `verification.txt` with logical "thinking" blocks and valid JSON subtasks.
