from pathlib import Path
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from config import SEARCH_URL, STATE_PATH, DEBUG_DIR


def clip(s, n=180):
    s = ' '.join((s or '').split())
    return s[:n]


def main():
    if not STATE_PATH.exists():
        raise RuntimeError('kimstudy_state.json이 없습니다. 먼저 python login_once.py 를 실행하세요.')

    DEBUG_DIR.mkdir(exist_ok=True)
    network_hits = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=str(STATE_PATH))
        page = context.new_page()

        def on_response(resp):
            try:
                req = resp.request
                rt = req.resource_type
                u = resp.url
                low = u.lower()
                if rt in {'xhr', 'fetch'} and any(k in low for k in ['tutee', 'student', 'lesson', 'offer', 'search', 'list']):
                    network_hits.append((resp.status, rt, u))
            except Exception:
                pass

        page.on('response', on_response)
        page.goto(SEARCH_URL, wait_until='networkidle', timeout=60000)
        page.wait_for_timeout(1500)

        anchors = page.locator('a[href]')
        anchor_rows = []
        for i in range(min(anchors.count(), 500)):
            a = anchors.nth(i)
            href = a.get_attribute('href') or ''
            text = clip(a.inner_text() if a.is_visible() else '')
            if href:
                anchor_rows.append((href, text))

        # Generic clickable DOM candidates. This is diagnostic only; nothing is clicked.
        clickable = page.evaluate("""
        () => {
          const els = [...document.querySelectorAll('button,[role="button"],[onclick],[tabindex],a')];
          const out = [];
          for (const el of els) {
            const t = (el.innerText || el.textContent || '').replace(/\\s+/g,' ').trim();
            if (!t || t.length < 8 || t.length > 500) continue;
            const r = el.getBoundingClientRect();
            if (r.width < 20 || r.height < 15) continue;
            out.push({
              tag: el.tagName,
              role: el.getAttribute('role') || '',
              href: el.getAttribute('href') || '',
              cls: String(el.className || '').slice(0,160),
              text: t.slice(0,220)
            });
          }
          return out.slice(0,500);
        }
        """)

        body = page.locator('body').inner_text(timeout=10000)
        (DEBUG_DIR / 'probe_body.txt').write_text(body, encoding='utf-8')
        (DEBUG_DIR / 'probe_anchors.txt').write_text(
            '\n'.join(f'{h}\t{t}' for h, t in anchor_rows), encoding='utf-8'
        )
        (DEBUG_DIR / 'probe_clickables.txt').write_text(
            '\n'.join(f"{x['tag']}\t{x['role']}\t{x['href']}\t{x['cls']}\t{x['text']}" for x in clickable),
            encoding='utf-8'
        )
        (DEBUG_DIR / 'probe_network.txt').write_text(
            '\n'.join(f'{s}\t{rt}\t{u}' for s, rt, u in network_hits), encoding='utf-8'
        )
        page.screenshot(path=str(DEBUG_DIR / 'probe.png'), full_page=True)

        print('\n=== 김과외 진단 결과 ===')
        print('현재 URL:', page.url)
        print('a[href] 개수:', anchors.count())
        print('클릭 후보 개수:', len(clickable))
        print('관련 XHR/fetch 개수:', len(network_hits))

        print('\n[학생/공고 관련 가능성이 높은 링크]')
        shown = 0
        for href, text in anchor_rows:
            low = (href + ' ' + text).lower()
            if any(k in low for k in ['tutee', '학생', '학부모', '생기부', '학종', '수시', '제안']):
                print('-', urljoin(page.url, href), '|', text)
                shown += 1
                if shown >= 30:
                    break
        if shown == 0:
            print('(일반 링크에서는 후보를 찾지 못함)')

        print('\n[관련 네트워크 요청]')
        for status, rt, u in network_hits[:30]:
            print('-', status, rt, u)
        if not network_hits:
            print('(관련 XHR/fetch를 찾지 못함)')

        print('\n상세 진단파일은 debug 폴더에 저장했습니다.')
        print('특히 probe_network.txt와 probe_clickables.txt가 중요합니다.')
        browser.close()


if __name__ == '__main__':
    main()
