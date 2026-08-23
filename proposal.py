from models import StudentLead

def generate_proposal(lead: StudentLead) -> StudentLead:
    reasons='\n'.join('• '+x for x in lead.score_reasons[:4])
    lead.proposal=f'''안녕하세요 😊\n학생 요청을 읽고 연락드립니다.\n\n🎓 고려대 공학 → 💊 부산대 약학\n\n• 고려대학교 산업경영공학과\n• 데이터과학 복수전공\n• 고려대 GPA 4.30 / 4.50\n• 부산대학교 약학대학 약학과 편입 · 현재 재학\n• 대통령과학장학금 수혜\n• NYU 교환학생\n• KAIST DSAIL Lab 연구 인턴\n• AI·데이터·바이오 연구·프로젝트 경험\n\n━━━━━━━━━━━━━━\n\n🔍 학생 상황에서 중요하게 본 부분\n\n{lead.request_text[:550]}\n\n{reasons}\n\n━━━━━━━━━━━━━━\n\n📚 수업 전 분석 자료\n\n• 현재 생기부\n• 내신·모의고사 및 선택과목\n• 기존 수행평가·세특·탐구보고서\n• 희망 대학·학과\n\n━━━━━━━━━━━━━━\n\n① 현재 기록 진단\n② 탐구 질문과 활동 방향 설계\n③ 자료 조사·보고서 구조 피드백\n④ 후속 탐구 및 면접 연결\n\n━━━━━━━━━━━━━━\n\n🗓️ 추천 진행 방식\n\n✨ {lead.program}\n\n━━━━━━━━━━━━━━\n\n🌱 수업 원칙\n\n• 생기부·세특·보고서를 대신 작성하지 않습니다.\n• 학생이 직접 이해하고 작성하도록 지도합니다.\n• 초안은 논리·근거·구조 중심으로 피드백합니다.\n• 면접에서도 자기 언어로 설명할 수 있도록 지도합니다.\n'''
    return lead
