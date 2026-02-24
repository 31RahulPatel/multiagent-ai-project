# Multi-Agent Website Builder with Google Gemini AI

A multi-agent autonomous system using **Google Gemini API** that collaboratively builds, tests, and deploys projects.

## Agents

1. **Coder Agent** - Generates code in ANY language/framework
2. **Tester Agent** - Creates appropriate tests
3. **User Simulation Agent** - Identifies issues
4. **Manager Agent** - Approves/rejects based on standards
5. **Deployment Agent** - Runs locally, detects errors, auto-fixes them

## Supported Tech Stacks

- **Frontend**: HTML/CSS/JS, React, Vue, Angular
- **Backend**: Python/Flask/Django, Node.js/Express, FastAPI
- **Full-stack**: MERN, MEAN, Django+React
- **Static Sites**: Pure HTML/CSS
- **Any language/framework** the AI can generate!

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set your Gemini API key
export GEMINI_API_KEY="your_gemini_api_key_here"
```

## Usage

```bash
python3 orchestrator.py
```

## How It Works

1. **Coder Agent** generates code in any language/framework
2. **Tester Agent** creates and runs appropriate tests
3. **User Agent** simulates usage and provides feedback
4. **Manager Agent** reviews and decides APPROVED/REJECTED
5. If rejected, feedback loops back for improvement
6. **Deployment Agent** asks to run locally, detects errors, auto-fixes them
7. Process repeats until approval (max 5 iterations)

## Customization

Edit the requirement in `orchestrator.py`:

```python
requirement = "Your custom website requirement here"
orchestrator.run(requirement)
```

## Files Generated

- `app.py` - Generated Flask application
- `test_app.py` - Generated pytest tests
- `state.json` - System state tracking
- `manager_decision.txt` - Latest manager decision
- `user_feedback.txt` - Latest user feedback
- `test_results.txt` - Latest test results
