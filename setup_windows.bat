@echo off
cd /d %~dp0
python -m pip install -r requirements.txt
if errorlevel 1 goto :error
python -m playwright install chromium
if errorlevel 1 goto :error
if not exist .env copy .env.example .env

echo.
echo 설치 완료.
echo 1. .env 파일에 NOTION_TOKEN을 입력하세요.
echo 2. python login_once.py 를 실행해 김과외 로그인 세션을 저장하세요.
echo 3. python test_notion.py 로 Notion 연결을 확인하세요.
pause
exit /b 0

:error
echo 설치 중 오류가 발생했습니다.
pause
exit /b 1
