import re
import json
from google.oauth2.service_account import Credentials
import gspread

# 1. Setup Google Sheets API
SHEET_NAME = "Copy of dataset IITTTTTTT"
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)

spreadsheet = client.open(SHEET_NAME)
sheet = spreadsheet.worksheet("A")

def parse_and_upload(file_path, num_to_copy):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to capture the full block per entry
    pattern = re.compile(
        r'\[INPUT\].*?Task\s+:\s+(.*?)\n.*?Level\s+:\s+(.*?)\n.*?\[THINKING PROCESS\](.*?)\n-{10,}.*?\[FINAL JSON OUTPUT\]\s*(.*?)(?=\n={10,}|$)',
        re.S
    )

    matches = list(pattern.finditer(content))
    
    rows_to_append = []
    copied_count = 0

    for match in matches:
        if copied_count >= num_to_copy:
            break

        task_val = match.group(1).strip()
        main_level = match.group(2).strip().lower()
        thinking_val = match.group(3).strip()
        json_str = match.group(4).strip()

        # Rule 1: Skip if the main input Level is low
        if main_level == "low":
            continue

        # Rule 2: Parse JSON to check internal IDs and internal Levels
        try:
            data = json.loads(json_str)
            subtasks = data.get("subtasks", [])

            # Skip if less than 4 IDs
            if len(subtasks) < 4:
                continue

            # Rule 3: Skip if ANY internal subtask level is "low"
            # This is the fix you asked for
            has_low_subtask = any(s.get("level", "").lower() == "low" for s in subtasks)
            if has_low_subtask:
                continue

        except Exception:
            continue

        # If it passes all filters, add to list
        rows_to_append.append([task_val, thinking_val, json_str])
        copied_count += 1

    if rows_to_append:
        sheet.append_rows(rows_to_append)
        print(f"✅ Success: {len(rows_to_append)} entries (High level with 4+ IDs and no low subtasks) copied.")
        
        clean = input("Clear verification.txt? (y/n): ")
        if clean.lower() == 'y':
            open(file_path, 'w').close()
            print("File cleared.")
    else:
        print("Done: No entries met your criteria (Check for 4+ IDs and no 'low' subtask levels).")

# --- Execution ---
try:
    selection = int(input("Enter the maximum number of valid tasks you want to copy: "))
    parse_and_upload("verification.txt", selection)
except Exception as e:
    print(f"An error occurred: {e}")