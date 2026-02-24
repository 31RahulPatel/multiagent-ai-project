# Multi-Agent Website Builder with Groq AI

A multi-agent autonomous system using **Groq API (Llama-3.1-8b-instant)** that collaboratively builds websites through iterative improvements.

## Agents

1. **Coder Agent** - Uses Groq AI to generate and improve Python/Flask code
2. **Tester Agent** - Uses Groq AI to create pytest tests
3. **User Simulation Agent** - Uses Groq AI to identify UX, validation, and security issues
4. **Manager Agent** - Uses Groq AI to approve or reject based on production standards

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set your Groq API key
export GROQ_API_KEY="your_groq_api_key_here"
```

## Usage

```bash
python3 orchestrator.py
```

## How It Works

1. **Coder Agent** generates code using Groq AI based on requirement
2. **Tester Agent** creates and runs tests using Groq AI
3. **User Agent** simulates usage and provides feedback using Groq AI
4. **Manager Agent** reviews and decides APPROVED/REJECTED using Groq AI
5. If rejected, feedback is used to improve in next iteration
6. Process repeats until approval (max 5 iterations)

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
