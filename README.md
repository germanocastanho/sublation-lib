# 🧠 Sublation

Classical boolean logic forces every proposition into exactly one of two states. That works well for most software, but it can't represent situations where a claim and its negation are both partially warranted, or where neither is warranted yet. As a solution, `Sublation` models truth as a relationship between a **thesis** and an **antithesis**, and derives a **synthesis** from how they interact — allowing states like contradiction and becoming to be detected rather than defined away.

# ✨ Main Features

- **Thesis** and **Antithesis** classes to represent claims and their negations.
- **Synthesis** class to represent the interaction between a thesis and an antithesis.
- Methods to detect **negation**, **contradiction**, **becoming**, and **sublation**.

# ✅ Prerequisites

- Python 3.12+ installed on your machine
- Astral Uv package manager (optional)
- Dependencies listed in `requirements.txt`

# ⚙️ Installation

### For regular use:

```bash
# Clone the repository
git clone https://github.com/germanocastanho/sublation-package
cd sublation-package/

# Create a venv (optional)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install sublation package
pip install -e .
```

### For development:

```bash
# Clone the repository
git clone https://github.com/germanocastanho/sublation-package
cd sublation-package/

# Create a venv (optional)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install sublation package
pip install -e ".[dev]"

# Run full test suite
pytest
```

# 🚀 Quick Start

```python
from sublation import Thesis, Antithesis, Synthesis

t = Thesis(True)
a = Antithesis(True)
s = Synthesis(t, a)

s.contradiction()       # True  — the tension is real and detectable
s.becoming()            # False — this is not a quiet resolution
s.sublation()           # True  — it doesn't collapse into falsehood

# The next round
t2 = s.as_thesis()
```

# 📜 Libre Software

If you have ideas for improvements or new features, please open an issue or submit a pull request! Make sure to follow the existing code style and include tests for any new functionality. This project is licensed under the MIT License. You are free to use, modify, and distribute this software. For more information, please refer to the [LICENSE](LICENSE) file.
