from notion_sync import get_data_source_id, query_existing

if __name__=='__main__':
    dsid=get_data_source_id()
    print('Notion 연결 성공')
    print('data_source_id:',dsid)
    hashes,urls=query_existing()
    print('기존 원문해시:',len(hashes))
    print('기존 URL:',len(urls))
