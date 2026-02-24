import os
from groq import Groq

class UserAgent:
    def __init__(self, workspace):
        self.workspace = workspace
        self.feedback_file = os.path.join(workspace, "user_feedback.txt")
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
    def simulate_usage(self, code_file):
        with open(code_file, 'r') as f:
            code = f.read()
        
        prompt = f"""You are a user testing this web application code. Identify issues:
- Missing validation
- UX gaps
- Unclear error handling
- Security weaknesses

CODE:
{code}

Respond with specific issues found, or "No critical issues found" if code is good."""
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.5
        )
        
        feedback = response.choices[0].message.content.strip()
        
        with open(self.feedback_file, 'w') as f:
            f.write(feedback)
        
        return feedback
