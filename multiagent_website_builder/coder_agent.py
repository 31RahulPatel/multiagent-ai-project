import os
import google.generativeai as genai

class CoderAgent:
    def __init__(self, workspace):
        self.workspace = workspace
        self.code_file = os.path.join(workspace, "output")
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        os.makedirs(self.code_file, exist_ok=True)
        
    def generate_code(self, requirement, feedback=None):
        if feedback:
            prompt = f"""You are an expert full-stack developer. Improve this project based on feedback.

REQUIREMENT: {requirement}

FEEDBACK:
{feedback}

Generate complete, production-quality files. Format:

### FILENAME: filename.ext
```
file content here
```

No explanations, only code."""
        else:
            prompt = f"""You are an expert full-stack developer creating a professional, production-ready project.

REQUIREMENT: {requirement}

CREATE A HIGH-QUALITY PROJECT WITH:

1. MODERN DESIGN:
   - Clean, professional UI/UX
   - Responsive design (mobile-first)
   - Modern color scheme and typography
   - Smooth animations and transitions
   - Professional spacing and layout

2. BEST PRACTICES:
   - Semantic HTML5
   - CSS Grid/Flexbox for layouts
   - Clean, organized code structure
   - Accessibility (ARIA labels, alt text)
   - SEO-friendly markup

3. FEATURES:
   - Interactive elements
   - Smooth scrolling
   - Hover effects
   - Professional navigation
   - Contact forms (if applicable)

4. CODE QUALITY:
   - Well-commented code
   - Modular CSS
   - Optimized performance
   - Cross-browser compatible

Generate ALL necessary files including:
- HTML files (semantic, accessible)
- CSS files (modern, responsive)
- JavaScript files (if needed for interactivity)
- README.md with setup instructions

Format your response as:

### FILENAME: path/to/filename.ext
```
file content here
```

Create a STUNNING, PROFESSIONAL project that rivals top portfolios. No explanations, only high-quality code."""
        
        response = self.model.generate_content(prompt)
        
        content = response.text.strip()
        self._parse_and_save_files(content)
        
        return self.code_file
    
    def _parse_and_save_files(self, content):
        import re
        pattern = r'### FILENAME: ([^\n]+)\n```(?:[a-z]*\n)?([\s\S]*?)```'
        matches = re.findall(pattern, content)
        
        if not matches:
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
