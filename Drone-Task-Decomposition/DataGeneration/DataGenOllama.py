import json
import re
import time
import csv
import os
import requests

# ==========================================
# CONFIGURATION
# ==========================================


buildings = {
    "Nalanda": {
        "name": "Nalanda",
        "type": "building",
        "shape": "Rectangular",
        "coordinates": {
            "corners": {
                "point_A": "22°19'04.6\"N 87°18'56.6\"E",
                "point_B": "22°18'55.5\"N 87°18'58.1\"E",
                "point_C": "22°19'05.3\"N 87°19'02.2\"E",
                "point_D": "22°18'56.4\"N 87°19'03.4\"E"
            },
            "middle_point": {
                "mid_AB": "22°19'00.05\"N 87°18'57.35\"E",
                "mid_BC": "22°18'56.0\"N 87°19'00.75\"E",
                "mid_CD": "22°19'00.85\"N 87°19'02.8\"E",
                "mid_DA": "22°19'05.0\"N 87°19'00.4\"E"
            },
            "centroid": "22°19'00.0\"N 87°19'00.0\"E",
            "altitude_data": {
                "perimeter_altitude": 6.0,
                "overhead_altitude": 8.5,
                "unit": "meters"
            }
        },
        "storey": "2"
    },

    "Tata Complex": {
        "name": "Tata Complex",
        "type": "open area",
        "shape": "Rectangular",
        "coordinates": {
            "corners": {
                "point_A": "22°19'02.1\"N 87°18'35.3\"E",
                "point_B": "22°19'01.3\"N 87°18'27.4\"E",
                "point_C": "22°18'52.4\"N 87°18'28.2\"E",
                "point_D": "22°18'52.8\"N 87°18'36.3\"E"
            },
            "middle_point": {
                "mid_AB": "22°19'01.7\"N 87°18'31.35\"E",
                "mid_BC": "22°18'52.05\"N 87°18'31.85\"E",
                "mid_CD": "22°18'52.6\"N 87°18'32.25\"E",
                "mid_DA": "22°19'00.25\"N 87°18'31.75\"E"
            },
            "centroid": "22°18'57.3\"N 87°18'31.9\"E",
            "altitude_data": {
                "perimeter_altitude": 6.0,
                "overhead_altitude": 8.5,
                "unit": "meters"
            }
        },
        "storey": "0"
    },

    "Takshashila": {
        "name": "Takshashila",
        "type": "building",
        "shape": "Rectangular",
        "coordinates": {
            "corners": {
                "point_A": "22°19'02.8\"N 87°18'42.0\"E",
                "point_B": "22°19'00.3\"N 87°18'42.5\"E",
                "point_C": "22°19'02.9\"N 87°18'44.8\"E",
                "point_D": "22°19'00.8\"N 87°18'45.1\"E"
            },
            "middle_point": {
                "mid_AB": "22°19'01.55\"N 87°18'42.25\"E",
                "mid_BC": "22°19'00.55\"N 87°18'43.8\"E",
                "mid_CD": "22°19'01.85\"N 87°18'44.95\"E",
                "mid_DA": "22°19'01.85\"N 87°18'43.4\"E"
            },
            "centroid": "22°19'01.8\"N 87°18'43.9\"E",
            "altitude_data": {
                "perimeter_altitude": 6.0,
                "overhead_altitude": 8.5,
                "unit": "meters"
            }
        },
        "storey": "2"
    },

    "Main Building": {
        "name": "Main Building",
        "type": "building",
        "shape": "Rectangular",
        "coordinates": {
            "corners": {
                "point_A": "22°19'11.4\"N 87°18'35.6\"E",
                "point_B": "22°19'10.1\"N 87°18'35.8\"E",
                "point_C": "22°19'10.1\"N 87°18'37.1\"E",
                "point_D": "22°19'11.8\"N 87°18'37.2\"E"
            },
            "middle_point": {
                "mid_AB": "22°19'10.75\"N 87°18'35.7\"E",
                "mid_BC": "22°19'10.95\"N 87°18'36.45\"E",
                "mid_CD": "22°19'10.95\"N 87°18'36.65\"E",
                "mid_DA": "22°19'10.75\"N 87°18'36.4\"E"
            },
            "centroid": "22°19'10.8\"N 87°18'36.4\"E",
            "altitude_data": {
                "perimeter_altitude": 6.0,
                "overhead_altitude": 8.5,
                "unit": "meters"
            }
        },
        "storey": "2"
    },

    "Gymkhana": {
        "name": "Gymkhana",
        "type": "building",
        "shape": "Rectangular",
        "coordinates": {
            "corners": {
                "point_A": "22°19'07.7\"N 87°18'08.9\"E",
                "point_B": "22°19'07.8\"N 87°18'10.0\"E",
                "point_C": "22°19'06.6\"N 87°18'10.2\"E",
                "point_D": "22°19'06.8\"N 87°18'08.6\"E"
            },
            "middle_point": {
                "mid_AB": "22°19'01.55\"N 87°18'42.25\"E",
                "mid_BC": "22°19'00.55\"N 87°18'43.8\"E",
                "mid_CD": "22°19'01.85\"N 87°18'44.95\"E",
                "mid_DA": "22°19'01.85\"N 87°18'43.4\"E"
            },
            "centroid": "22°19'07.2\"N 87°18'09.5\"E",
            "altitude_data": {
                "perimeter_altitude": 6.0,
                "overhead_altitude": 8.5,
                "unit": "meters"
            }
        },
        "storey": "2"
    }
}



MODEL_NAME = "deepseek-coder-v2:16b-lite-instruct-q4_K_M"
OLLAMA_URL = "http://localhost:11434/api/generate"

OUT_CSV = "decompositions.csv"
OUT_TXT = "verificationtest.txt"
DELAY_BETWEEN_TASKS = 1.0

SYSTEM_PROMPT = """
You are a Drone Swarm Logic Core. Decompose HIGH tasks into 3 to 5 MID level subtasks.

-------------------------
CRITICAL RULE: MAX 5 SUBTASKS
-------------------------
- **HARD LIMIT:** You MUST NOT output more than 5 subtasks.
- **TRUNCATION PROTOCOL:** If a logical decomposition requires >5 steps (e.g., 4 walls + 4 corners = 8), you MUST DROP the least critical steps to fit the limit.
- **PRIORITY:** Keep Centroids > Keep Walls > Keep Corners.
- If you output 6 or more subtasks, the system will crash.

-------------------------
NAMING & VOCABULARY
-------------------------
1. **Building Name:** Every subtask string MUST end with "... of <Target_Name>".
   - Example: "Scan Wall AB of Nalanda"
2. **Geometry:** Use "Wall" (not Edge) and "Corner" (not Point).
3. **Verbs:** Use specific verbs (Thermal Scan, Structural Check, Hover, Monitor).

-------------------------
DECOMPOSITION STRATEGIES
-------------------------
1. "ROUTINE" (Serial): [1]->[2]->[3]. Scan Walls + Centroid. (Max 5).
2. "URGENT" (Parallel): []. Scan Centroid + 2-3 Corners. (Max 4-5).
3. "FOCUSED" (Spot Check): []. Scan only the specific side mentioned. (1-2 tasks).

-------------------------
LEVEL SEMANTICS
-------------------------
- HIGH → MID (Sectors/Walls).
- MID → LOW (Atomic: move -> hover -> capture).
- LOW → Return unchanged.

-------------------------
OUTPUT FORMAT
-------------------------
<think>
1. Strategy Selection (Routine/Urgent/Focused).
2. Token Selection (Check if count > 5. If yes, prune list).
3. Formatting (Add "... of Building").
</think>
{
  "subtasks": [
    { "id": 1, "task": "...", "level": "...", "dep": [...] }
  ]
}

-------------------------
FEW-SHOT EXAMPLES (Strictly <= 5)
-------------------------

### EXAMPLE 1 — COMPROMISE (Pruning to fit 5)
Input:
{ "task": "Complete exterior scan of Nalanda", "level": "high", "target": "Nalanda", "context": {...} }
Output:
<think>
1. Full scan usually needs 4 Walls + 4 Corners (8 steps).
2. CONSTRAINT: Max 5 allowed.
3. DECISION: Keep 4 Walls + 1 Centroid. Drop Corners.
</think>
{
  "subtasks": [
    { "id": 1, "task": "Scan Wall AB of Nalanda (use mid_AB)", "level": "mid", "dep": [] },
    { "id": 2, "task": "Scan Wall BC of Nalanda (use mid_BC)", "level": "mid", "dep": [1] },
    { "id": 3, "task": "Scan Wall CD of Nalanda (use mid_CD)", "level": "mid", "dep": [2] },
    { "id": 4, "task": "Scan Wall DA of Nalanda (use mid_DA)", "level": "mid", "dep": [3] },
    { "id": 5, "task": "Overhead Centroid View of Nalanda (use centroid)", "level": "mid", "dep": [4] }
  ]
}

### EXAMPLE 2 — FOCUSED (Small count)
Input:
{ "task": "Check entrance cracks at Gymkhana", "level": "high", "target": "Gymkhana", "context": {...} }
Output:
<think>
1. Entrance is Wall DA.
2. Only check Wall DA and adjacent corners. Total 3 steps. Fits limit.
</think>
{
  "subtasks": [
    { "id": 1, "task": "Inspect Wall DA of Gymkhana (use mid_DA)", "level": "mid", "dep": [] },
    { "id": 2, "task": "Inspect Corner D of Gymkhana (use point_D)", "level": "mid", "dep": [] },
    { "id": 3, "task": "Inspect Corner A of Gymkhana (use point_A)", "level": "mid", "dep": [] }
  ]
}

-------------------------
START
-------------------------
"""

def call_local_ai(input_json):
    prompt = f"{SYSTEM_PROMPT}\n\nINPUT TASK:\n{json.dumps(input_json)}\n\nOutput:"
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 1000
        }
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        raw_text = response.json().get("response", "")

        # 1. Extract Thinking Process
        think_match = re.search(r"<think>(.*?)</think>", raw_text, re.DOTALL | re.IGNORECASE)
        thinking = think_match.group(1).strip() if think_match else "Reasoning: Geometric decomposition for autonomous scan."

        # 2. Extract JSON
        json_start = raw_text.find("{")
        json_end = raw_text.rfind("}") + 1
        json_str = raw_text[json_start:json_end]
        json_str = json_str.replace("'", '"')
        json_str = re.sub(r",\s*}", "}", json_str)
        subtask_obj = json.loads(json_str)

        # 3. AUTO-REPAIR Logic (Fix IDs, Levels, and Tags)
        subs = subtask_obj.get("subtasks", [])
        for i, sub in enumerate(subs):
            sub["id"] = i + 1
            sub["level"] = "mid"
            sub["dep"] = [i] if i > 0 else []
            
            # Re-enforce Coordinate Tags if AI misses them
            t = sub.get("task", "")
            if "Wall AB" in t and "(use mid_AB)" not in t: sub["task"] = "Scan Wall AB of Nalanda (use mid_AB)"
            elif "Wall BC" in t and "(use mid_BC)" not in t: sub["task"] = "Scan Wall BC of Nalanda (use mid_BC)"
            elif "Wall CD" in t and "(use mid_CD)" not in t: sub["task"] = "Scan Wall CD of Nalanda (use mid_CD)"
            elif "Wall DA" in t and "(use mid_DA)" not in t: sub["task"] = "Scan Wall DA of Nalanda (use mid_DA)"
            elif "Corner A" in t and "(use point_A)" not in t: sub["task"] = "Inspect Corner A of Nalanda (use point_A)"
            elif "Corner B" in t and "(use point_B)" not in t: sub["task"] = "Inspect Corner B of Nalanda (use point_B)"
            elif "Corner C" in t and "(use point_C)" not in t: sub["task"] = "Inspect Corner C of Nalanda (use point_C)"
            elif "Corner D" in t and "(use point_D)" not in t: sub["task"] = "Inspect Corner D of Nalanda (use point_D)"
            elif ("Centroid" in t or "Overhead" in t) and "(use centroid)" not in t: sub["task"] = "Overhead View of Nalanda (use centroid)"

        subtask_obj["subtasks"] = subs[:5]
        return {"thinking": thinking, "subtask_json": subtask_obj}
    except Exception as e:
        print(f"  ❌ AI Error: {e}")
        return None

def append_files(record, idx):
    # CSV Write
    file_exists = os.path.exists(OUT_CSV)
    with open(OUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["task_json", "thinking", "subtask_json"])
        writer.writerow([json.dumps(record["task_json"]), record["thinking"], json.dumps(record["subtask_json"])])
    
    # TXT Write (Restored Original Format)
    block = f"""
================================================================================
ENTRY #{idx}
================================================================================
[INPUT]
Task  : {record['task_json']['task']}
Level : {record['task_json'].get('level', 'high')}
Target: Nalanda

--------------------------------------------------------------------------------
[THINKING PROCESS]
{record['thinking']}

--------------------------------------------------------------------------------
[FINAL JSON OUTPUT]
{json.dumps(record['subtask_json'], indent=4)}

"""
    with open(OUT_TXT, "a", encoding="utf-8") as f:
        f.write(block)

def main():
    TASKS = [

                {"task": "Analyze the number of cracks in the walls of Nalanda", "level": "high"},


    ]

    print(f"Starting Offline processing with DeepSeek...")
    for i, t in enumerate(TASKS):
        print(f"[{i+1}/{len(TASKS)}] Processing: {t['task'][:40]}...")
        out = call_local_ai(t)
        if out:
            record = {"task_json": t, "thinking": out["thinking"], "subtask_json": out["subtask_json"]}
            append_files(record, i+1)
            print("  ✅ Success.")
        time.sleep(DELAY_BETWEEN_TASKS)

if __name__ == "__main__":
    main()