from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright
from config import SEARCH_URL, STATE_PATH, DEBUG_DIR

BLOCKED = {'/tutee/list','/tutee/bookmark','/tutee/offer','/tutee/myOffer/form','/tutee/myoffer/form','/tutee/myOffer','/tutee/myoffer'}

def save_login_state():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=False)
        context=browser.new_context()
        page=context.new_page()
        page.goto('https://kimstudy.com/tutee/list',wait_until='domcontentloaded')
        print('\n브라우저에서 직접 로그인하세요.')
        print('로그인 후 학생 목록이 보이면 이 터미널에서 Enter를 누르세요.\n')
        input()
        context.storage_state(path=str(STATE_PATH))
        browser.close()
        print(f'세션 저장 완료: {STATE_PATH}')

def is_student_detail(href:str)->bool:
    if not href: return False
    full=urljoin('https://kimstudy.com',href); p=urlparse(full)
    path=p.path.rstrip('/') or '/'; low=path.lower()
    if 'kimstudy.com' not in p.netloc.lower(): return False
    if path in BLOCKED or low in {x.lower() for x in BLOCKED}: return False
    if not low.startswith('/tutee/'): return False
    if any(x in low for x in ['/bookmark','/offer','/myoffer','/list','/profile','/setting','/mypage']): return False
    tail=path.split('/tutee/',1)[1].strip('/'); parts=[x for x in tail.split('/') if x]
    if not parts: return False
    candidate=parts[1] if parts[0].lower() in {'detail','view'} and len(parts)>=2 else parts[0]
    compact=candidate.replace('-','')
    return (compact.isdigit() and len(compact)>=3) or (len(compact)>=8 and compact.isalnum()) or any(k in p.query.lower() for k in ['tuteeid=','tutee_id=','id='])

def collect_detail_urls(page):
    urls=[]; anchors=page.locator('a[href]')
    for i in range(anchors.count()):
        href=anchors.nth(i).get_attribute('href') or ''
        if is_student_detail(href): urls.append(urljoin(page.url,href))
    return list(dict.fromkeys(urls))

def scrape_once(limit:int=30):
    if not STATE_PATH.exists(): raise RuntimeError('kimstudy_state.json이 없습니다. 먼저 python login_once.py 를 실행하세요.')
    DEBUG_DIR.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        context=browser.new_context(storage_state=str(STATE_PATH))
        page=context.new_page(); page.goto(SEARCH_URL,wait_until='networkidle',timeout=60000)
        body=page.locator('body').inner_text(timeout=10000)
        urls=collect_detail_urls(page)
        (DEBUG_DIR/'detected_urls.txt').write_text('\n'.join(urls),encoding='utf-8')
        if not urls:
            (DEBUG_DIR/'list.html').write_text(page.content(),encoding='utf-8')
            (DEBUG_DIR/'list_text.txt').write_text(body,encoding='utf-8')
            page.screenshot(path=str(DEBUG_DIR/'list.png'),full_page=True)
            browser.close()
            raise RuntimeError('학생 상세 링크를 확실하게 식별하지 못했습니다. 잘못된 메뉴를 저장하지 않기 위해 수집을 중단했습니다.')
        results=[]
        for url in urls[:limit]:
            detail=context.new_page()
            try:
                detail.goto(url,wait_until='networkidle',timeout=60000)
                text=detail.locator('body').inner_text(timeout=10000)
                signals=['학생','학부모','학년','수업','과외','희망','학교','목표','제안']
                if len(text.strip())>=120 and sum(1 for s in signals if s in text)>=2: results.append((url,text))
            finally: detail.close()
        browser.close(); return results
