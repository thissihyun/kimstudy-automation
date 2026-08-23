from dataclasses import dataclass, field
from typing import Optional

@dataclass
class StudentLead:
    nickname: str = ''
    author_type: str = ''
    grade: str = ''
    track: str = '미정'
    gender: str = ''
    school: str = ''
    current_level: str = ''
    grades: str = ''
    goal: str = ''
    target_university: str = ''
    target_major: str = ''
    subjects: list[str] = field(default_factory=list)
    focus_areas: list[str] = field(default_factory=list)
    request_text: str = ''
    budget_text: str = ''
    online_possible: Optional[bool] = None
    region: str = ''
    proposal_count: Optional[int] = None
    urgent: Optional[bool] = None
    modified_at: str = ''
    url: str = ''
    raw_text: str = ''
    score: int = 0
    grade_label: str = ''
    score_reasons: list[str] = field(default_factory=list)
    program: str = '기타'
    proposal: str = ''
    source_hash: str = ''
