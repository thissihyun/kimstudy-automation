import re
from models import StudentLead

def score_lead(lead: StudentLead) -> StudentLead:
    t = lead.raw_text
    score = 45
    reasons = []
    boosts = [(14,r'생기부|학교생활기록부|학종|학생부종합','생기부·학종 요청과 직접 일치'),(10,r'세특|수행평가|활동\s*설계|전공\s*탐구','세특·활동 설계 수요'),(9,r'보고서|소논문|논문|데이터\s*분석|탐구','보고서·탐구·데이터형 과제와 높은 연관'),(8,r'면접|꼬리질문|예상질문','면접 지도 가능'),(8,r'AI|인공지능|데이터|공학|기계|신소재|DGIST|KAIST|POSTECH','공학·AI·데이터 배경과 직접 연결'),(8,r'약학|의학|의약|생명|바이오|신약','약학·바이오 경험과 직접 연결'),(7,r'고1|고2|고등학교\s*[12]학년','장기 관리 가능성이 높은 학년'),(5,r'화상|온라인','화상 진행 가능')]
    for pts, pat, reason in boosts:
        if re.search(pat,t,re.I): score += pts; reasons.append(reason)
    if lead.proposal_count is not None:
        if lead.proposal_count <= 15: score += 5; reasons.append('제안 경쟁이 비교적 낮음')
        elif lead.proposal_count >= 60: score -= 6; reasons.append('제안 경쟁이 높은 편')
    score=max(0,min(100,score)); lead.score=score
    lead.grade_label='🔥 A급' if score>=85 else ('🌿 B급' if score>=70 else '⚪ C급')
    lead.score_reasons=reasons[:5] or ['프로필 정보가 적어 보수적으로 평가']
    return lead
