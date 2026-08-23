import re
from models import StudentLead

def select_program(lead: StudentLead) -> StudentLead:
    t=lead.raw_text
    if re.search(r'약대\s*편입|약학대학\s*편입',t): lead.program='약대 편입'
    elif lead.grade=='고3' and re.search(r'면접|예상질문|꼬리질문|제시문',t): lead.program='학종 면접 집중 대비'
    elif lead.grade=='고3' and re.search(r'수시|학종\s*가능|지원\s*전략|6장',t): lead.program='고3 수시 지원 전략'
    elif re.search(r'외대부고|외고|국제고|자사고|특목고|고입',t): lead.program='특목고·자소서·면접'
    elif lead.grade in ('고1','고2') and re.search(r'체계적|장기|한\s*학기|관리|DGIST|KAIST|POSTECH',t): lead.program='한 학기 생기부 관리'
    elif re.search(r'세특|수행평가|보고서|소논문|탐구\s*주제|자료\s*조사',t): lead.program='세특·수행평가·전공탐구'
    elif re.search(r'생기부|학종|진로\s*변경|방향|가능성',t): lead.program='생기부 정밀 진단'
    else: lead.program='기타'
    return lead
