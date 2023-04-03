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

def getsupporting(desertionno) :
    conn, cursor = getDBConn_Cursor()
    
    ### SQL 구문 작성
    sql = """
            select desertionno, filename, popfile  from dog_notice 
            where dog_notice.desertionno =: desertionno
            UNION ALL 
            select desertionno, filename, popfile  from dog_protect
            where dog_protect.desertionno =: desertionno
    """
    ### 구문을 서버에게 보내서 요청하고, 결과 받아오기
    cursor.execute(sql, desertionno = desertionno)
    
    rows = cursor.fetchone()
    
    ### 조회결과가 없으면  바로 리턴
    if rows == None :
        ###DB연결 해제하기
        DBClose(cursor, conn)
        ### 성공여부
        return {"rs" : "no"}
    
    ### 컬럼명 조회하기
    colname = cursor.description
    
    ### {} 형태로 변환
    dict_col = getFetchOne(colname, rows)
    ### 성공여부저장
    dict_col["rs"] = "yes"
    
    ### DB연결 해제하기
    DBClose(cursor, conn)
    
    return dict_col

##################### 후원하기
def getsupport(mem_id, desertionno, support, money) :

    conn, cursor = getDBConn_Cursor()
    
    sql = """
            INSERT INTO DOG_SUPPORT
            ( mem_id, desertionno, support, money)
            VALUES (
                '{}',
                {},
                '{}',
                {}
            )
    """.format(mem_id, desertionno, support, money)
    
    cursor.execute(sql)
    
    conn.commit()

    DBClose(cursor, conn)
    return "OK"

def getspt_list(mem_id) :
    conn, cursor = getDBConn_Cursor()
    
    # 정기후원 검색
    sql= """
            Select * From dog_support
            where mem_id = '{}' and support = '정기후원'
        """.format(mem_id)
    cursor.execute(sql)
    spt_eve = cursor.fetchall()
    colname1 = cursor.description
    spt_eve = getFetchAll(colname1,spt_eve)
    
    # 정기 후원 금액
    sql= """
            select sum(money) from dog_support
            where support='정기후원' and mem_id = '{}'
        """.format(mem_id)
    cursor.execute(sql)
    eve_money = cursor.fetchone()
    
    # 단일후원 검색
    sql= """
            Select * From dog_support
            where mem_id ='{}' and support = '단일후원'
        """.format(mem_id)
    cursor.execute(sql)
    spt_one = cursor.fetchall()
    colname2 = cursor.description
    spt_one = getFetchAll(colname2,spt_one)
    # 단일후원 금액
    sql= """
            select sum(money) from dog_support
            where support='단일후원' and mem_id='{}'
        """.format(mem_id)
    cursor.execute(sql)
    one_money = cursor.fetchone()
    
    DBClose(cursor, conn)
    
    return spt_eve, spt_one, eve_money, one_money

def getsptview(desertionno) :
    conn, cursor = getDBConn_Cursor()
    
    ### SQL 구문 작성
    sql = """
            select *  from dog_notice 
            where dog_notice.desertionno =: desertionno
            UNION ALL 
            select *  from dog_protect
            where dog_protect.desertionno =: desertionno
    """
    ### 구문을 서버에게 보내서 요청하고, 결과 받아오기
    cursor.execute(sql, desertionno = desertionno)
    
    rows = cursor.fetchone()
    
    ### 조회결과가 없으면  바로 리턴
    if rows == None :
        ###DB연결 해제하기
        DBClose(cursor, conn)
        ### 성공여부
        return {"rs" : "no"}
    
    ### 컬럼명 조회하기
    colname = cursor.description
    
    ### {} 형태로 변환
    dict_col = getFetchOne(colname, rows)
    ### 성공여부저장
    dict_col["rs"] = "yes"
    
    ### DB연결 해제하기
    DBClose(cursor, conn)
    
    return dict_col