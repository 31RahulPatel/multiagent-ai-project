import json
import os
from coder_agent import CoderAgent
from tester_agent import TesterAgent
from user_agent import UserAgent
from manager_agent import ManagerAgent

class Orchestrator:
    def __init__(self, workspace):
        self.workspace = workspace
        self.state_file = os.path.join(workspace, "state.json")
        self.coder = CoderAgent(workspace)
        self.tester = TesterAgent(workspace)
        self.user = UserAgent(workspace)
        self.manager = ManagerAgent(workspace)
        self.max_iterations = 5
        
    def run(self, requirement):
        self._update_state(requirement=requirement, iteration=0, status="running")
        
        for iteration in range(1, self.max_iterations + 1):
            print(f"\n{'='*60}")
            print(f"ITERATION {iteration}")
            print(f"{'='*60}\n")
            
            state = self._read_state()
            feedback = state.get("feedback", [])
            feedback_text = "\n".join(feedback) if feedback else None
            
            print("🔧 CODER AGENT: Generating code...")
            code_file = self.coder.generate_code(requirement, feedback_text)
            print(f"   Code written to: {code_file}")
            
            print("\n🧪 TESTER AGENT: Creating tests...")
            test_file = self.tester.generate_tests(code_file)
            print(f"   Tests written to: {test_file}")
            
            print("\n🧪 TESTER AGENT: Running tests...")
            test_results = self.tester.run_tests()
            print(f"   Test results:\n{test_results[:200]}...")
            
            print("\n👤 USER AGENT: Simulating usage...")
            user_feedback = self.user.simulate_usage(code_file)
            print(f"   Feedback:\n{user_feedback}")
            
            print("\n👔 MANAGER AGENT: Reviewing...")
            decision = self.manager.review(requirement, code_file, test_results, user_feedback)
            print(f"   Decision: {decision}")
            
            self._update_state(
                iteration=iteration,
                status="approved" if "APPROVED" in decision else "rejected",
                manager_decision=decision,
                feedback=[user_feedback] if "REJECTED" in decision else []
            )
            
            if "APPROVED" in decision:
                print(f"\n✅ PROJECT APPROVED after {iteration} iteration(s)")
                print(f"\n📁 Output files:")
                print(f"   - {code_file}")
                print(f"   - {test_file}")
                return True
            else:
                print(f"\n❌ REJECTED - Starting next iteration...")
        
        print(f"\n⚠️  Max iterations ({self.max_iterations}) reached without approval")
        return False
    
    def _read_state(self):
        with open(self.state_file, 'r') as f:
            return json.load(f)
    
    def _update_state(self, **kwargs):
        state = self._read_state()
        state.update(kwargs)
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

if __name__ == "__main__":
    workspace = os.path.dirname(os.path.abspath(__file__))
    orchestrator = Orchestrator(workspace)
    
    requirement = "Build a simple Flask web application with a homepage and API endpoint"
    orchestrator.run(requirement)
