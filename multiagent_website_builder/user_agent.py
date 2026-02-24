import os
import google.generativeai as genai

class UserAgent:
    def __init__(self, workspace):
        self.workspace = workspace
        self.feedback_file = os.path.join(workspace, "user_feedback.txt")
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def simulate_usage(self, code_file):
        files = []
        for root, dirs, filenames in os.walk(code_file):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as f:
                    files.append(f"{filename}:\n{f.read()}\n")
        
        all_code = "\n".join(files)
        
        is_static = any('.html' in f for f in files) and not any('.py' in f or '.js' in f or 'package.json' in f for f in files)
        
        if is_static:
            prompt = f"""You are reviewing a static HTML/CSS website. Check for:

1. DESIGN QUALITY:
   - Is the design modern and professional?
   - Is it responsive (mobile-friendly)?
   - Are colors and typography well-chosen?
   - Are there smooth transitions/animations?

2. CODE QUALITY:
   - Is HTML semantic and accessible?
   - Is CSS well-organized?
   - Are there any broken elements?

3. USER EXPERIENCE:
   - Is navigation intuitive?
   - Are interactive elements working?
   - Is content well-structured?

CODE:
{all_code[:3000]}

Respond with "No critical issues found" if the website is high-quality and professional, or list specific improvements needed."""
        else:
            prompt = f"""You are a senior developer reviewing this project for quality.

Check for:
- Code quality and organization
- Security vulnerabilities
- Missing features from requirement
- UX/UI issues
- Performance problems
- Missing error handling

PROJECT CODE:
{all_code[:3000]}

Respond with specific issues found, or "No critical issues found" if code is excellent."""
        
        response = self.model.generate_content(prompt)
        
        feedback = response.text.strip()
        
        with open(self.feedback_file, 'w') as f:
            f.write(feedback)
        
        return feedback
