@echo off
cd /d %~dp0

echo [1/2] GitHub 최신 코드 가져오는 중...
git pull
if errorlevel 1 goto :error

echo [2/2] 김과외 파이프라인 실행 중...
python pipeline.py
if errorlevel 1 goto :error

echo.
echo 완료되었습니다.
pause
exit /b 0

:error
echo.
echo 오류가 발생했습니다. 위 메시지를 ChatGPT에 보내주세요.
pause
exit /b 1
