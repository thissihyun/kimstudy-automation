import requests
from datetime import datetime, timezone, timedelta
from config import NOTION_TOKEN, NOTION_DATABASE_ID, NOTION_DATA_SOURCE_ID

API='https://api.notion.com/v1'
HEADERS={'Authorization':f'Bearer {NOTION_TOKEN}','Notion-Version':'2025-09-03','Content-Type':'application/json'}
_CACHE=None

def _check(r,action):
    if r.ok:return
    try: detail=r.json()
    except Exception: detail=r.text
    raise RuntimeError(f'Notion API 오류 ({action}) HTTP {r.status_code}\n{detail}')

def get_data_source_id():
    global _CACHE
    if _CACHE:return _CACHE
    if NOTION_DATA_SOURCE_ID:_CACHE=NOTION_DATA_SOURCE_ID;return _CACHE
    r=requests.get(f'{API}/databases/{NOTION_DATABASE_ID}',headers=HEADERS,timeout=30);_check(r,'database 조회')
    sources=r.json().get('data_sources') or []
    if not sources: raise RuntimeError("Notion DB에서 data source를 찾지 못했습니다. DB에 Integration을 연결하세요.")
    _CACHE=sources[0]['id'];return _CACHE

def query_existing():
    dsid=get_data_source_id(); hashes=set(); urls=set(); cursor=None
    while True:
        payload={'page_size':100}
        if cursor:payload['start_cursor']=cursor
        r=requests.post(f'{API}/data_sources/{dsid}/query',headers=HEADERS,json=payload,timeout=30);_check(r,'data source query')
        data=r.json()
        for page in data.get('results',[]):
            props=page.get('properties',{})
            h=''.join(x.get('plain_text','') for x in props.get('원문해시',{}).get('rich_text',[]))
            u=props.get('김과외 URL',{}).get('url')
            if h:hashes.add(h)
            if u:urls.add(u)
        if not data.get('has_more'):break
        cursor=data.get('next_cursor')
    return hashes,urls

def _text(v):return {'rich_text':[{'type':'text','text':{'content':(v or '')[:2000]}}]}
def _title(v):return {'title':[{'type':'text','text':{'content':(v or '')[:200]}}]}
def _select(v):return {'select':{'name':v}} if v else {'select':None}
def _multi(v):return {'multi_select':[{'name':x} for x in v]}
def _num(v):return {'number':v}
def _checkb(v):return {'checkbox':bool(v)}
def _url(v):return {'url':v or None}
def _date(v):return {'date':{'start':v}} if v else {'date':None}

def create_lead(lead):
    dsid=get_data_source_id(); today=datetime.now(timezone(timedelta(hours=9))).date().isoformat()
    title=' / '.join(x for x in [lead.grade,lead.track,lead.nickname] if x) or '김과외 신규 학생'
    props={'학생/공고':_title(title),'적합도':_num(lead.score),'등급':_select(lead.grade_label),'상태':_select('신규'),'학년':_select(lead.grade or '기타'),'계열':_select(lead.track or '미정'),'요청분야':_multi(lead.subjects),'제안경쟁':_num(lead.proposal_count),'화상가능':_checkb(lead.online_possible is True),'지역':_text(lead.region),'학교':_text(lead.school),'현재수준':_text(lead.current_level),'목표':_text(lead.goal),'요청사항':_text(lead.request_text),'추천프로그램':_select(lead.program),'김과외 URL':_url(lead.url),'발견일':_date(today),'원문해시':_text(lead.source_hash),'알림대상':_checkb(lead.score>=85)}
    blocks=[]
    def heading(s):return {'object':'block','type':'heading_2','heading_2':{'rich_text':[{'type':'text','text':{'content':s}}]}}
    def para(s):return {'object':'block','type':'paragraph','paragraph':{'rich_text':[{'type':'text','text':{'content':s}}]}}
    blocks+=[heading('🤖 자동 분석'),para(f'적합도 {lead.score}점 · {lead.grade_label}\n추천 프로그램: {lead.program}\n'+'\n'.join('• '+x for x in lead.score_reasons)),heading('✉️ 맞춤 제안서')]
    for i in range(0,len(lead.proposal),1900):blocks.append(para(lead.proposal[i:i+1900]))
    blocks.append(heading('📋 원문'))
    for i in range(0,len(lead.raw_text),1900):blocks.append(para(lead.raw_text[i:i+1900]))
    payload={'parent':{'type':'data_source_id','data_source_id':dsid},'properties':props,'children':blocks[:100]}
    r=requests.post(f'{API}/pages',headers=HEADERS,json=payload,timeout=30);_check(r,'lead page 생성')
    return r.json().get('url','')
