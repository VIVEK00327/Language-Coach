"""Shared data contract. Every ML module and the web app use these types.
Do not change without telling the lead (Role 1) and updating docs/PRD.md (section 4)."""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


@dataclass
class PhonemeResult:
    expected: Optional[str]   # None = extra sound spoken
    spoken: Optional[str]     # None = sound missing
    correct: bool


@dataclass
class WordResult:
    word: str
    score: float              # 0-100
    phonemes: List[PhonemeResult] = field(default_factory=list)


@dataclass
class AssessmentResult:
    language: str
    target_text: str
    overall_score: float      # 0-100
    words: List[WordResult] = field(default_factory=list)
    feedback: List[str] = field(default_factory=list)
    timing: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
