import cx_Oracle as ora

### DB연결, 접속, 커서받아오기 
# - 리턴값 : 커서
def getDBConn_Cursor() :
    try :
        # 데이터소스(datasource)는 서버로부터 
        # 데이터베이스에 대해 연결을 구축하기 위해 사용하는 이름이다.
        # 이 이름은 데이터베이스에 쿼리를 만들 때 공통적으로 사용된다.
        ### 서버찾아가기
        dsn = ora.makedsn("localhost", 1521, "xe")
        
        ### 서버와 접속하기
        conn = ora.connect("pet", "dbdb", dsn)

        ### 커서 받아오기
        cursor = conn.cursor()
    except :
        return False

    return conn, cursor   

def getFetchOne(colname, row): 
    ### 컬럼명만 추출하여 리스트에 담기
    col = []

    for c in colname:
        col.append(c[0].lower())     

    ### 튜플을 딕셔너리로 변환하기
    dict_col = {}
    
    for i in range(0, len(row), 1) :
        dict_col[col[i]] = row[i]
    
    return dict_col

def DBClose(cursor, conn):
    ### 커서 역할 끝내기(반납)
    cursor.close()
    
    ### 접속 끊기(통로가 사라짐)
    conn.close()

### 신고정보 저장하기
def ReportInsert(data) :

    conn, cursor = getDBConn_Cursor()
    
    sql = """
            SELECT NVL(MAX(REQ_NO), 0) + 1  as req_no 
            FROM 
            DOG_FIND
    """
    ### 구문을 서버에게 보내서 요청하고, 결과 받아오기
    cursor.execute(sql)
    
    row = cursor.fetchone()
    
    ### 컬럼명 조회하기
    colname = cursor.description

    ### {}형태로 변환
    dict_col = getFetchOne(colname, row)
        
    try:         
            
        ### SQL 구문 작성
        sql = """
                INSERT INTO DOG_FIND
                ( REQ_NO, F_MEM_ID, POPFILE, HAPPENDT, HAPPENPLACE,
                    KINDCD, COLORCD, AGE, PROCESSSTATE, SEXCD,
                    NEUTERYN, SPECIALMARK )
                VALUES (
                    {},
                    '{}',
                    '{}',
                    '{}',
                    '{}',
                    '{}',
                    '{}',
                    '{}',
                    '{}',
                    '{}',
                    '{}',
                    '{}'
                )
        """.format(dict_col["req_no"], data["f_mem_id"], data["popfile"],
                    data["happendt"], data["happenplace"], data["kindcd"],
                    data["colorcd"], data["age"], data["processstate"],
                    data["sexcd"], data["neuteryn"],
                    data["specialmark"]
                    )
        
        cursor.execute(sql)
        
        conn.commit()
    except:    
        DBClose(cursor, conn)
        return "no"

    DBClose(cursor, conn)
    return "ok"