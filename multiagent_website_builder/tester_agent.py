import os
from groq import Groq

class TesterAgent:
    def __init__(self, workspace):
        self.workspace = workspace
        self.test_file = os.path.join(workspace, "test_app.py")
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
    def generate_tests(self, code_file):
        files = []
        for root, dirs, filenames in os.walk(code_file):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as f:
                    files.append(f"{filename}:\n{f.read()}\n")
        
        all_code = "\n".join(files)
        
        prompt = f"""Generate appropriate tests for this project. Use the right testing framework for the language.

CODE:
{all_code[:3000]}

For Python: use pytest
For JavaScript: use Jest or Mocha
For HTML/CSS: use basic validation tests

Output ONLY valid test code. No explanations."""
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=2000
        )
        
        tests = response.choices[0].message.content.strip()
        tests = tests.replace("```python", "").replace("```", "").strip()
        
        with open(self.test_file, 'w') as f:
            f.write(tests)
        
        return self.test_file
    
    def run_tests(self):
        result_file = os.path.join(self.workspace, "test_results.txt")
        os.system(f"cd {self.workspace} && python3 -m pytest {self.test_file} -v > {result_file} 2>&1")
        
        if os.path.exists(result_file):
            with open(result_file, 'r') as f:
                return f.read()
        return "Tests not executed"
