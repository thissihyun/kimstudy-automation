import time
from datetime import datetime
from config import POLL_SECONDS
from pipeline import run_once

if __name__=='__main__':
    print(f'김과외 감시 시작 · {POLL_SECONDS}초 간격')
    while True:
        try:
            created=run_once()
            print(datetime.now().isoformat(timespec='seconds'),f'신규 {len(created)}건')
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(datetime.now().isoformat(timespec='seconds'),'ERROR:',e)
        time.sleep(POLL_SECONDS)
