# Kimstudy Automation

김과외 신규 학생을 탐지해 구조화하고, 적합도/등급/추천 프로그램/맞춤 제안서를 생성한 뒤 Notion CRM에 저장하는 자동화입니다.

## 흐름
김과외 → Playwright → 신규 학생 상세 수집 → 파싱 → 적합도 점수화 → 프로그램 추천 → 제안서 생성 → Notion CRM → A급 알림

자동 제안 전송은 하지 않습니다. CAPTCHA/접근 제한 우회도 하지 않습니다.

## 최초 설치 (Windows)
```powershell
python -m pip install -r requirements.txt
python -m playwright install chromium
Copy-Item .env.example .env
python login_once.py
```

`.env`에 Notion 토큰을 넣고 DB에 Integration을 연결한 뒤:
```powershell
python test_notion.py
python pipeline.py
```

지속 감시:
```powershell
python watch_kimstudy.py
```

## 업데이트 후 실행
로컬 저장소에서:
```powershell
git pull
python pipeline.py
```

또는 `update_and_run.bat` 더블클릭.

## 절대 커밋 금지
- `.env`
- `kimstudy_state.json`
- `debug/`
