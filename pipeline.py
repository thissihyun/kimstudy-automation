from kimstudy import scrape_once
from parser import parse_detail
from scorer import score_lead
from program_selector import select_program
from proposal import generate_proposal
from notion_sync import query_existing, create_lead

def run_once(limit=30):
    hashes,urls=query_existing(); created=[]
    for url,raw in scrape_once(limit):
        lead=parse_detail(raw,url)
        if lead.source_hash in hashes or lead.url in urls: continue
        lead=score_lead(lead); lead=select_program(lead); lead=generate_proposal(lead)
        notion_url=create_lead(lead)
        created.append((lead.score,lead.grade_label,lead.program,notion_url))
        hashes.add(lead.source_hash); urls.add(lead.url)
    return created

if __name__=='__main__':
    created=run_once(); print(f'신규 저장: {len(created)}건')
    for row in sorted(created,reverse=True): print(row)
