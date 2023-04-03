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

### 여러건 처리 : [{}, {}] 형태로 반환
def getFetchAll(colname, row): 
    ### 컬럼명만 추출하여 리스트에 담기
    col = []

    for c in colname:
        col.append(c[0].lower())     

    ### 키, 값 형태로 딕셔너리 생성
    list_row = []
    
    for columns in row :
        ### 딕셔너리 초기화
        dict_col = {}
        
        ### 인덱스 번호 활용
        ### 4개 튜플 반복
        for i in range(0, len(columns), 1) :
    #         print("key[{}]/ value [{}]".format(col[i], columns[i]))
            ### 컬럼명(key) : value 넣기 
            dict_col[col[i]] = columns[i]

        list_row.append(dict_col)
    
    return list_row

def DBClose(cursor, conn):
    ### 커서 역할 끝내기(반납)
    cursor.close()
    
    ### 접속 끊기(통로가 사라짐)
    conn.close()

def getMemberList() :
    conn, cursor = getDBConn_Cursor()
    
    ### SQL 구문 작성
    sql = """
            select mem_id, mem_name
                from member
    """
    ### 구문을 서버에게 보내서 요청하고, 결과 받아오기
    cursor.execute(sql)
    
    ### 받아온 결과를 달라고 요청
    row = cursor.fetchall()
    
    ### 컬럼명 조회하기
    colname = cursor.description
    

    list_row = getFetchAll(colname, row)
    
    DBClose(cursor, conn)
    
    return list_row


def MemberInsert(mem_id, mem_pass, mem_name, mem_email) :
    try:
        conn, cursor = getDBConn_Cursor()
        
    

        sql = """Insert Into member(mem_id, mem_pass, mem_name, mem_email) 
                        Values(:mem_id, :mem_pass, :mem_name, :mem_email)"""
                        
        cursor.execute(sql, mem_id=mem_id, mem_pass=mem_pass, mem_name=mem_name, mem_email=mem_email)
        
        conn.commit()
    except:    
        DBClose(cursor, conn)
        return "no"
    
    DBClose(cursor, conn)
    return "OK"

def MemberDelete(mem_id, mem_pass, mem_name, mem_email):
    try:
        conn, cursor = getDBConn_Cursor()
        
        sql = """Delete Into member(mem_id, mem_pass, mem_name, mem_email) 
                        Values(:mem_id, :mem_pass, :mem_name, :mem_email)"""
                        
        cursor.execute(sql, mem_id=mem_id, mem_pass=mem_pass, mem_name=mem_name, mem_email=mem_email)
        
        conn.commit()
    except:    
        DBClose(cursor, conn)
        return "no"
    
    DBClose(cursor, conn)
    return "OK"

def getFetchOne(colname,row):
    ### 컬럼명 조회하기
    
    col=[]

    for i in colname:
        col.append(i[0].lower())
        
    dict_col ={}
    for i in range(0,len(row),1):
            dict_col[col[i]] =row[i]
    
    return dict_col 

def getLogin(p_id, p_pass) :
    ### DB접속하기
    conn, cursor = getDBConn_Cursor()
    
    sql = """
            Select * From member
                where mem_id =: mem_id 
                    And mem_pass =: mem_pass
    """
    cursor.execute(sql, mem_id=p_id, mem_pass=p_pass)
    
    rows = cursor.fetchone()
    
    ### 조회결과가 없으면 바로 리턴
    if rows == None :
        ### DB연결 해제하기
        DBClose(cursor, conn)
        ## 성공여부
        return {"rs" : "no"}
    
    ### 컬럼명 조회하기
    colname = cursor.description  
    
    ### {}형태로 변환
    dict_col = getFetchOne(colname, rows)
    
    ### 성공 여부 저장
    dict_col["rs"] = "yes"
    
    ### DB연결 해제하기
    DBClose(cursor, conn)
    
    return dict_col

def MemberUpdate(mem_id, mem_pass, mem_name, mem_email) :

    try:
        conn, cursor = getDBConn_Cursor()
        
        
        sql = """Update member 
                Set
                    mem_pass = '{0}', 
                    mem_email = '{1}',
                    mem_name = '{2}'
                where mem_id='{3}'
                    """.format(mem_pass, mem_email, mem_name, mem_id )           
                    
        cursor.execute(sql)
        
        conn.commit()
    except:    
        DBClose(cursor, conn)
        return "no", sql
    
    DBClose(cursor, conn)
    return "OK", sql

def getMember(mem_id) :
    conn, cursor = getDBConn_Cursor()
    
    sql= """
            Select * From member
            where mem_id =: mem_id 
        """
    cursor.execute(sql, mem_id=mem_id)

    rows = cursor.fetchone()
    colname = cursor.description

    dict_col = getFetchOne(colname,rows)
    DBClose(cursor, conn)
    
    return dict_col