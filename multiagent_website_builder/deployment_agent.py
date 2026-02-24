import os
import subprocess
import time
import signal
from groq import Groq

class DeploymentAgent:
    def __init__(self, workspace):
        self.workspace = workspace
        self.output_dir = os.path.join(workspace, "output")
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.process = None
        self.port = 5000
        
    def deploy_and_test(self, requirement):
        print("\n🚀 DEPLOYMENT AGENT: Analyzing project structure...")
        
        # Detect project type and run command
        run_command = self._detect_run_command()
        
        if not run_command:
            print("   ⚠️  Could not determine how to run this project")
            return True
        
        print(f"   Detected run command: {run_command}")
        print(f"   Port: {self.port}")
        
        # Ask user permission
        print(f"\n❓ Would you like to run the project locally on port {self.port}? (yes/no): ", end="")
        response = input().strip().lower()
        
        if response not in ['yes', 'y']:
            print("   Skipping deployment test")
            return True
        
        # Try to run the project
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            print(f"\n🔄 Attempt {attempt}/{max_attempts}: Starting project...")
            
            success, error = self._run_project(run_command)
            
            if success:
                print(f"\n✅ Project running successfully on port {self.port}!")
                print(f"   Access it at: http://localhost:{self.port}")
                print("\n   Press Ctrl+C to stop the server...")
                try:
                    self.process.wait()
                except KeyboardInterrupt:
                    self._stop_project()
                    print("\n   Server stopped.")
                return True
            else:
                print(f"\n❌ Error detected:\n{error}")
                
                if attempt < max_attempts:
                    print(f"\n🔧 Auto-fixing errors...")
                    self._auto_fix_errors(error, requirement)
                else:
                    print(f"\n⚠️  Max attempts reached. Manual intervention needed.")
                    return False
        
        return False
    
    def _detect_run_command(self):
        files = os.listdir(self.output_dir)
        
        # Static HTML (prioritize this)
        if 'index.html' in files:
            # Check if it's truly static (no build tools needed)
            has_package_json = 'package.json' in files
            if has_package_json:
                # Check if package.json has build scripts
                try:
                    import json
                    with open(os.path.join(self.output_dir, 'package.json'), 'r') as f:
                        pkg = json.load(f)
                        # If no build script, treat as static
                        if 'scripts' not in pkg or 'build' not in pkg.get('scripts', {}):
                            return f"cd {self.output_dir} && python3 -m http.server {self.port}"
                except:
                    pass
                # Has package.json with build - skip deployment
                return None
            else:
                # Pure static HTML
                return f"cd {self.output_dir} && python3 -m http.server {self.port}"
        
        # Python Flask/Django
        elif 'app.py' in files:
            return f"cd {self.output_dir} && python3 app.py"
        elif 'manage.py' in files:
            return f"cd {self.output_dir} && python3 manage.py runserver {self.port}"
        
        # Node.js (only if npm is available)
        elif 'package.json' in files:
            # Check if npm exists
            import shutil
            if shutil.which('npm'):
                return f"cd {self.output_dir} && npm install && npm start"
            else:
                print("   ⚠️  Node.js project detected but npm not installed. Skipping deployment.")
                return None
        
        return None
    
    def _run_project(self, command):
        try:
            # Install dependencies first
            self._install_dependencies()
            
            # Run the project
            self.process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a bit to see if it starts successfully
            time.sleep(3)
            
            # Check if process is still running
            if self.process.poll() is None:
                return True, None
            else:
                _, stderr = self.process.communicate()
                return False, stderr
                
        except Exception as e:
            return False, str(e)
    
    def _install_dependencies(self):
        files = os.listdir(self.output_dir)
        
        # Python dependencies
        if 'requirements.txt' in files:
            print("   Installing Python dependencies...")
            subprocess.run(
                f"cd {self.output_dir} && pip install -r requirements.txt",
                shell=True,
                capture_output=True
            )
        
        # Node.js dependencies
        if 'package.json' in files:
            print("   Installing Node.js dependencies...")
            subprocess.run(
                f"cd {self.output_dir} && npm install",
                shell=True,
                capture_output=True
            )
    
    def _auto_fix_errors(self, error, requirement):
        # Read all project files
        files_content = []
        for root, dirs, files in os.walk(self.output_dir):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        rel_path = os.path.relpath(filepath, self.output_dir)
                        files_content.append(f"{rel_path}:\n{f.read()}\n")
                except:
                    pass
        
        all_code = "\n".join(files_content)
        
        prompt = f"""Fix this project error.

REQUIREMENT: {requirement}

CURRENT CODE:
{all_code[:2000]}

ERROR:
{error}

Generate fixed files in this format:

### FILENAME: path/to/filename.ext
```
fixed code here
```

Only include files that need changes. No explanations."""
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.2,
            max_tokens=3000
        )
        
        content = response.choices[0].message.content.strip()
        self._apply_fixes(content)
        print("   ✅ Fixes applied")
    
    def _apply_fixes(self, content):
        import re
        pattern = r'### FILENAME: ([^\n]+)\n```(?:[a-z]*\n)?([\s\S]*?)```'
        matches = re.findall(pattern, content)
        
        for filename, code in matches:
            filepath = os.path.join(self.output_dir, filename.strip())
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else self.output_dir, exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(code.strip())
    
    def _stop_project(self):
        if self.process:
            try:
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            except:
                self.process.terminate()
            self.process = None
