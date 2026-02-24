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
        
        is_static = 'index.html' in all_code and '.py' not in all_code and 'package.json' not in all_code
        
        if is_static:
            prompt = f"""Review this static website as a senior design/engineering lead.

REQUIREMENT: {requirement}

CODE:
{all_code}

USER FEEDBACK:
{user_feedback}

APPROVE ONLY IF:
- Design is modern, professional, visually appealing
- Fully responsive (mobile, tablet, desktop)
- Clean, semantic HTML5
- Well-organized, modern CSS
- Smooth animations/transitions
- Excellent user experience
- Accessible (ARIA, alt text)
- All feedback issues resolved

Be STRICT - this should be portfolio-quality work.

Respond ONLY:
"APPROVED"
or
"REJECTED: <specific reason>"
"""
        else:
            prompt = f"""You are a senior engineering manager reviewing for production.

REQUIREMENT: {requirement}

CODE:
{all_code}

TEST RESULTS:
{test_results[:500]}

USER FEEDBACK:
{user_feedback}

APPROVE ONLY IF:
- Production-ready, well-architected
- All tests pass
- Security best practices
- No hardcoded secrets
- Excellent error handling
- Clean, maintainable code
- All feedback resolved

Be STRICT - enterprise-grade quality required.

Respond ONLY:
"APPROVED"
or
"REJECTED: <specific reason>"
"""
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        decision = response.choices[0].message.content.strip()
        
        with open(self.decision_file, 'w') as f:
            f.write(decision)
        
        return decision
