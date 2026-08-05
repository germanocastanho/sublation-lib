# 🧠 Sublation

This library formalizes dialectical logic as a case of four-valued reasoning
(true / false / contradictory / indeterminate), grounded in Belnap–Dunn
logic (FDE) and the bilattice structure behind paraconsistent annotated
logics such as Eτ. Inspired by Hegel's dialectical logic, it provides a framework for reasoning in a rigorous way. Try it out!

# ✨ Main Features

- **Thesis** and **Antithesis** classes to represent claims and their negations.
- **Synthesis** class to represent the interaction between a thesis and an antithesis.
- Methods to detect **negation**, **contradiction**, **becoming**, and **sublation**.
- **TruthValue** class backing all three, an evidence pair (`mu` for, `lam` against) making contradiction and indeterminacy representable.

# ✅ Prerequisites

- Python 3.12+ installed on your machine
- Astral uv package manager (optional)
- Dependencies listed in `requirements.txt`

# ⚙️ Installation

### For regular use:

```bash
# Clone the repository
git clone https://github.com/germanocastanho/sublation-lib
cd sublation-lib/

# Create a venv (optional)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install sublation package
pip install -e .
```

Or just `pip install sublation`!

### For development:

```bash
# Clone the repository
git clone https://github.com/germanocastanho/sublation-lib
cd sublation-lib/

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

If you have ideas for improvements or new features, please open an issue or submit a pull request. Make sure to follow the existing code style and include tests for any new functionality. Licensed under the MIT License, so you are free to use, modify, and distribute this software. Please refer to the [LICENSE](LICENSE) for more!
