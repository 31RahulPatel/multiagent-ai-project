import os
from groq import Groq

class CoderAgent:
    def __init__(self, workspace):
        self.workspace = workspace
        self.code_file = os.path.join(workspace, "app.py")
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
    def generate_code(self, requirement, feedback=None):
        if os.path.exists(self.code_file) and feedback:
            with open(self.code_file, 'r') as f:
                existing_code = f.read()
            prompt = f"""Improve this code based on feedback.

EXISTING CODE:
{existing_code}

FEEDBACK:
{feedback}

Output ONLY valid Python code. No explanations."""
        else:
            prompt = f"""Create a minimal Flask web application for: {requirement}

Requirements:
- Use Flask
- Clean, production-ready code
- Proper error handling
- Input validation
- No hardcoded secrets

Output ONLY valid Python code. No explanations."""
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.3
        )
        
        code = response.choices[0].message.content.strip()
        code = code.replace("```python", "").replace("```", "").strip()
        
        with open(self.code_file, 'w') as f:
            f.write(code)
        
        return self.code_file
