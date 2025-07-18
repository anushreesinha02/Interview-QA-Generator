def build_prompt(role, tools, experience, count):
    if not isinstance(tools, list):
        tools = []
    tools_str = ", ".join(tools) if tools else "general tools"
    experience_str = experience if experience else "entry-level"

    return  (
    f"You are an expert technical interviewer.\n\n"
    f"Generate {count} unique, high-quality interview questions for a candidate applying for the role of '{role}' "
    f"with an experience level of {experience_str}.\n"
    f"Focus specifically on the following tools and skills: {tools_str}.\n\n"
    f"For each question:\n"
    f"- Provide a realistic, high-quality sample answer.\n"
    f"- Provide a brief critique (1–2 sentences) evaluating the quality of the answer.\n"
    f"- Include a relevant code snippet or real-world example if applicable.\n\n"
    f"Return the output as a JSON array (no markdown), where each item has this structure:\n"
    f'{{\n'
    f'  "question": "Your question text here",\n'
    f'  "answer": "Your sample answer here",\n'
    f'  "critique": "Your critique of the answer here"\n'
    f'}}\n\n'
    f"Important rules:\n"
    f"- Return only a **valid JSON array** of objects.\n"
    f"- Do NOT include any explanations, markdown formatting, or headers.\n"
    f"- Ensure the JSON is strictly syntactically correct and parsable by standard JSON parsers.\n"
)