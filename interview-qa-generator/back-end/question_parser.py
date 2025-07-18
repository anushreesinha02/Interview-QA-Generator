import json
import re
import ast

def parse_qa(raw_output):
    # ✅ Case 1: Already parsed Python list of dicts
    if isinstance(raw_output, list):
        if all(isinstance(q, dict) and 'question' in q and 'answer' in q for q in raw_output):
            return raw_output

    # ✅ Case 2: JSON or stringified output
    if isinstance(raw_output, str):
        raw_output = raw_output.strip()

        # 🔍 Try full JSON string first
        try:
            parsed = json.loads(raw_output)
            if isinstance(parsed, list) and all(isinstance(q, dict) for q in parsed):
                return parsed
        except Exception as e:
            print("json.loads failed:", e)

        # 🛠 Try to extract the first list-like structure (e.g., [ {...}, {...} ])
        match = re.search(r"\[.*?\]", raw_output, re.DOTALL)
        if match:
            list_str = match.group(0)

            # ✅ Repair malformed list JSON
            list_str = re.sub(r',\s*(\}|\])', r'\1', list_str)         # Remove trailing commas
            list_str = re.sub(r'\}\s*\{', '}, {', list_str)             # Fix missing commas between objects
            list_str = re.sub(r'"\s*(")', r'", \1', list_str)         # Fix missing commas between fields

            # ✅ Escape all unescaped newlines/tabs inside JSON string values
            list_str = re.sub(r'(?<!\\)\n', r'\\n', list_str)
            list_str = re.sub(r'(?<!\\)\t', r'\\t', list_str)

            list_str = list_str.strip()

            # 🧪 Debugging aid
            # print("Final cleaned JSON snippet:\n", list_str[:500])

            try:
                return json.loads(list_str)
            except Exception as e:
                print("JSON recovery failed:", e)

            # 🛠 Try Python-safe fallback
            try:
                parsed = ast.literal_eval(list_str)
                if isinstance(parsed, list) and all(isinstance(q, dict) for q in parsed):
                    return parsed
            except Exception as e:
                print("ast.literal_eval failed:", e)

    print("parse_qa() could not extract Q&A.")
    return []

