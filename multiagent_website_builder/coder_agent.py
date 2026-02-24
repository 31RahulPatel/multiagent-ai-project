import os
from groq import Groq

class CoderAgent:
    def __init__(self, workspace):
        self.workspace = workspace
        self.code_file = os.path.join(workspace, "output")
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        os.makedirs(self.code_file, exist_ok=True)
        
    def generate_code(self, requirement, feedback=None):
        main_file = os.path.join(self.code_file, "index.html")
        
        if feedback:
            prompt = f"""Improve this project based on feedback.

REQUIREMENT: {requirement}

FEEDBACK:
{feedback}

Generate complete files needed (any language/framework). Format:

### FILENAME: filename.ext
```
file content here
```

No explanations, only code."""
        else:
            prompt = f"""Create a complete project for: {requirement}

Use the BEST technology stack for this requirement (HTML/CSS/JS, React, Python/Flask, Node.js, etc.).

Generate ALL necessary files including:
- Source code files
- Configuration files (package.json, requirements.txt, etc.)
- README.md with setup instructions

Format your response as:

### FILENAME: path/to/filename.ext
```
file content here
```

Make it production-ready, clean, and minimal. No explanations, only code."""
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content.strip()
        self._parse_and_save_files(content)
        
        return self.code_file
    
    def _parse_and_save_files(self, content):
        import re
        pattern = r'### FILENAME: ([^\n]+)\n```(?:[a-z]*\n)?([\s\S]*?)```'
        matches = re.findall(pattern, content)
        
        if not matches:
            # Fallback: detect language and save appropriately
            if "<!DOCTYPE" in content or "<html" in content:
                ext = "index.html"
            elif "def " in content or "import " in content:
                ext = "app.py"
            elif "function" in content or "const" in content:
                ext = "app.js"
            else:
                ext = "output.txt"
            
            main_file = os.path.join(self.code_file, ext)
            content = re.sub(r'```[a-z]*\n', '', content)
            content = content.replace("```", "").strip()
            with open(main_file, 'w') as f:
                f.write(content)
        else:
            for filename, code in matches:
                filepath = os.path.join(self.code_file, filename.strip())
                os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else self.code_file, exist_ok=True)
                with open(filepath, 'w') as f:
                    f.write(code.strip())
