"""
Copyleft 2026, Germano Castanho
Licensed under the MIT License
"""

from . import operators  # noqa: F401
from .core import Antithesis, Synthesis, Thesis
from .truths import TruthValue

__all__ = ["Antithesis", "Synthesis", "Thesis", "TruthValue"]
__version__ = "0.4.1"
