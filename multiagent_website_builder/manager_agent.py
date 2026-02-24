import os
from groq import Groq

class ManagerAgent:
    def __init__(self, workspace):
        self.workspace = workspace
        self.decision_file = os.path.join(workspace, "manager_decision.txt")
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
    def review(self, requirement, code_file, test_results, user_feedback):
        files = []
        for root, dirs, filenames in os.walk(code_file):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as f:
                    files.append(f"{filename}:\n{f.read()}\n")
        
        all_code = "\n".join(files)[:2000]
        
        # Check if it's a static HTML/CSS project
        is_static = 'index.html' in all_code and '.py' not in all_code and 'package.json' not in all_code
        
        if is_static:
            prompt = f"""Review this static HTML/CSS website for production.

REQUIREMENT: {requirement}

CODE:
{all_code}

USER FEEDBACK:
{user_feedback}

For static sites, approve if:
- HTML structure is valid
- CSS is present
- Meets basic requirement
- No broken code

Ignore: API security, backend validation, database issues (not applicable to static sites)

Respond ONLY:
"APPROVED"
or
"REJECTED: <reason>"
"""
        else:
            prompt = f"""You are a senior engineering manager. Review this project for production readiness.

REQUIREMENT: {requirement}

PROJECT CODE:
{all_code}

TEST RESULTS:
{test_results[:500]}

USER FEEDBACK:
{user_feedback}

APPROVAL CRITERIA:
- Code satisfies requirement
- Tests are meaningful (or not needed for static sites)
- Feedback issues resolved
- No security issues
- No hardcoded secrets
- Proper dependencies listed
- Works for any tech stack (Python, Node.js, HTML/CSS, React, etc.)

Respond with ONLY:
"APPROVED"
or
"REJECTED: <specific technical reason>"
"""
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.1,
            max_tokens=500
        )
        
        decision = response.choices[0].message.content.strip()
        
        with open(self.decision_file, 'w') as f:
            f.write(decision)
        
        return decision
