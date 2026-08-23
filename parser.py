import hashlib
import re
from models import StudentLead

GRADE_PATTERNS = [('고3', r'고\s*3|고등학교\s*3학년'),('고2', r'고\s*2|고등학교\s*2학년'),('고1', r'고\s*1|고등학교\s*1학년'),('중3', r'중\s*3|중학교\s*3학년'),('중2', r'중\s*2|중학교\s*2학년'),('중1', r'중\s*1|중학교\s*1학년')]

CATEGORY_RULES = [('생기부', r'생기부|학교생활기록부'),('학종', r'학종|학생부종합'),('수시컨설팅', r'수시\s*(지원|컨설팅|전략)|6장'),('세특·활동', r'세특|활동\s*설계|전공\s*탐구'),('수행평가', r'수행평가'),('보고서·소논문', r'보고서|소논문|논문|탐구\s*보고'),('면접', r'면접|꼬리질문|예상질문'),('특목고', r'외대부고|외고|국제고|자사고|특목고|고입'),('약대편입', r'약대\s*편입|약학대학\s*편입')]

def parse_detail(raw_text: str, url: str) -> StudentLead:
    lead = StudentLead(raw_text=raw_text.strip(), url=url)
    lines = [x.strip() for x in raw_text.splitlines() if x.strip()]
    lead.nickname = lines[0][:80] if lines else '김과외 학생'
    for grade, pattern in GRADE_PATTERNS:
        if re.search(pattern, raw_text, re.I):
            lead.grade = grade; break
    if re.search(r'\b이과\b|자연계|과학중점', raw_text): lead.track = '이과'
    elif re.search(r'\b문과\b|인문계', raw_text): lead.track = '문과'
    lead.online_possible = True if re.search(r'화상|온라인', raw_text) else None
    m = re.search(r'(?:제안|지원|경쟁)\s*(?:수|건수)?\s*[:：]?\s*(\d+)\s*건', raw_text)
    lead.proposal_count = int(m.group(1)) if m else None
    lead.subjects = [name for name, pat in CATEGORY_RULES if re.search(pat, raw_text, re.I)]
    lead.request_text = raw_text[-1800:].strip()
    lead.source_hash = hashlib.sha256((url.strip()+'\n'+lead.raw_text).encode('utf-8')).hexdigest()
    return lead
