import os
from groq import Groq

class UserAgent:
    def __init__(self, workspace):
        self.workspace = workspace
        self.feedback_file = os.path.join(workspace, "user_feedback.txt")
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
    def simulate_usage(self, code_file):
        files = []
        for root, dirs, filenames in os.walk(code_file):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as f:
                    files.append(f"{filename}:\n{f.read()}\n")
        
        all_code = "\n".join(files)
        
        # Check if it's a static HTML/CSS project
        is_static = any('.html' in f for f in files) and not any('.py' in f or '.js' in f or 'package.json' in f for f in files)
        
        if is_static:
            prompt = f"""You are reviewing a static HTML/CSS website. Be lenient - static sites don't need:
- API validation
- Backend security
- Database handling

Only flag CRITICAL issues like:
- Broken HTML structure
- Missing essential CSS
- Broken links

CODE:
{all_code[:3000]}

Respond with "No critical issues found" if the HTML/CSS is functional, or list only CRITICAL issues."""
        else:
            prompt = f"""You are a user testing this project. Identify issues:
- Missing validation
- UX gaps  
- Unclear error handling
- Security weaknesses
- Design issues
- Missing dependencies
- Configuration issues

PROJECT CODE:
{all_code[:3000]}

Respond with specific issues found, or "No critical issues found" if code is good."""
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=1500
        )
        
        feedback = response.choices[0].message.content.strip()
        
        with open(self.feedback_file, 'w') as f:
            f.write(feedback)
        
        return feedback
