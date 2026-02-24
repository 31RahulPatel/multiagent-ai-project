import os
from groq import Groq

class ManagerAgent:
    def __init__(self, workspace):
        self.workspace = workspace
        self.decision_file = os.path.join(workspace, "manager_decision.txt")
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
    def review(self, requirement, code_file, test_results, user_feedback):
        with open(code_file, 'r') as f:
            code = f.read()
        
        prompt = f"""You are a senior engineering manager. Review this code for production readiness.

REQUIREMENT: {requirement}

CODE:
{code}

TEST RESULTS:
{test_results[:500]}

USER FEEDBACK:
{user_feedback}

APPROVAL CRITERIA:
- Code satisfies requirement
- Tests are meaningful
- Feedback issues resolved
- No security issues
- No hardcoded secrets

Respond with ONLY:
"APPROVED"
or
"REJECTED: <specific technical reason>"
"""
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.1
        )
        
        decision = response.choices[0].message.content.strip()
        
        with open(self.decision_file, 'w') as f:
            f.write(decision)
        
        return decision
