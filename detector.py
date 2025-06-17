import re
from enum import Enum
from typing import List, Dict, Optional

# Objection Categories
class ObjectionCategory(str, Enum):
    PRICE = "Price"
    AUTHORITY = "Authority"
    NEED = "Need"
    TRUST = "Trust"
    TIMING = "Timing"
    COMPETITION = "Competition"
    GENERAL = "General"

# Pattern class
class ObjectionPattern:
    def __init__(self, pattern: str, category: ObjectionCategory, confidence: float = 0.8, is_regex: bool = False):
        self.pattern = pattern
        self.category = category
        self.confidence = confidence
        self.is_regex = is_regex

    def match(self, text: str) -> Optional[ObjectionCategory]:
        if self.is_regex:
            return self.category if re.search(self.pattern, text, re.IGNORECASE) else None
        return self.category if self.pattern.lower() in text.lower() else None

# ObjectionDetector engine
class ObjectionDetector:
    def __init__(self):
        self.patterns = self._initialize_patterns()
        self.responses = self._initialize_responses()

    def _initialize_patterns(self) -> List[ObjectionPattern]:
        return [
            ObjectionPattern(r"\b(too expensive|costs? too much|can't afford|over budget|price is high)\b", ObjectionCategory.PRICE, 0.9, True),
            ObjectionPattern("expensive", ObjectionCategory.PRICE, 0.8),
            ObjectionPattern("not in our budget", ObjectionCategory.PRICE, 0.9),
            ObjectionPattern("already have a vendor", ObjectionCategory.COMPETITION, 0.9),
            ObjectionPattern("not priority", ObjectionCategory.TIMING, 0.8),
            ObjectionPattern("not the decision maker", ObjectionCategory.AUTHORITY, 0.9),
            ObjectionPattern("happy with our current", ObjectionCategory.NEED, 0.7),
            ObjectionPattern("never heard of your company", ObjectionCategory.TRUST, 0.7),
            ObjectionPattern("not interested", ObjectionCategory.GENERAL, 0.9),
        ]

    def _initialize_responses(self) -> Dict[ObjectionCategory, List[str]]:
        return {
            ObjectionCategory.PRICE: [
                "Highlight ROI and long-term cost savings and Break down cost per user/month to show value"
            ],
            ObjectionCategory.AUTHORITY: [
                "Ask who else should be involved in the decision",
                "Offer to present to the decision-making team"
            ],
            ObjectionCategory.NEED: [
                "Identify pain points they might not have considered",
                "Show how current solution may have hidden costs"
            ],
            ObjectionCategory.TRUST: [
                "Share customer testimonials and case studies",
                "Offer a pilot program or trial period"
            ],
            ObjectionCategory.TIMING: [
                "Understand their timeline and constraints",
                "Show cost of delaying implementation"
            ],
            ObjectionCategory.COMPETITION: [
                "Highlight unique differentiators",
                "Offer to match or beat competitor pricing"
            ],
            ObjectionCategory.GENERAL: [
                "Ask clarifying questions to understand concerns",
                "Reframe the conversation around their goals"
            ]
        }

    def detect(self, text: str) -> Optional[ObjectionCategory]:
        for pattern in self.patterns:
            match = pattern.match(text)
            if match:
                return match
        return None

    def suggest_response(self, category: ObjectionCategory) -> str:
        return self.responses[category][0] if category in self.responses else "Let's discuss more."
