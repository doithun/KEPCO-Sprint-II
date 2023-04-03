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

def getFetchOne(colname, row) :   # 매개변수로 받아온 colname과 row를 받아서 사용할거야
    ## 컬럼명만 추출하여 리스트에 담기
    col = []
    for c in colname : 
        # col.append(c[0])            # 컬럼명이 대문자로 추출됨
        col.append(c[0].lower())      # 대문자인 컬럼명 소문자로 변환하기
        
    # 칼럼명과 그 값 교차시키기기
    dict_col ={}
    for i in range(0, len(row), 1) :
        dict_col[col[i]]=row[i]
        # print("key[{}]/ value[{}]".format(col[i], colums[i]))
    
    return dict_col

def getNotice() :
    conn, cursor = getDBConn_Cursor()
    
    ### SQL 구문 작성
    sql = """
            select substr(happendt, 0,4)||'-'||substr(happendt, 5,2) ||'-'|| substr(happendt, 7,2) as happendt,req_no,desertionno,filename,happenplace,kindcd,colorcd,age,weight,noticeno,
                    noticesdt,noticeedt,popfile,processstate,sexcd,neuteryn,specialmark,carenm,caretel,careaddr,orgnm,chargenm,officetel,noticecomment
                        from dog_notice
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

def getNoticeView(desertionno) :
    conn, cursor = getDBConn_Cursor()
    
    ### SQL 구문 작성
    sql = """
            select substr(happendt, 0,4)||'-'||substr(happendt, 5,2) ||'-'|| substr(happendt, 7,2) as happendt,req_no,desertionno,filename,happenplace,kindcd,colorcd,age,weight,noticeno,
                    noticesdt,noticeedt,popfile,processstate,sexcd,neuteryn,specialmark,carenm,caretel,careaddr,orgnm,chargenm,officetel,noticecomment
                        from dog_notice where desertionno =: desertionno
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

#########################################    search    #############################################
def getNoitceSearch(s_table, s_col, keyword) :
    conn, cursor = getDBConn_Cursor()
    
    sql = """
            select * from {}
            where {} like '%{}%'
        """.format(s_table, s_col, keyword)

    ### 구문을 서버에게 보내서 요청하고, 결과 받아오기
    #cursor.execute(sql, s_table=s_table, s_col=s_col, keyword=keyword)
    cursor.execute(sql)
    
    rows = cursor.fetchall()
    
    ### 조회결과가 없으면  바로 리턴
    if rows == None :
        ###DB연결 해제하기
        DBClose(cursor, conn)
        ### 성공여부
        return {"rs" : "no"}
    
    ### 컬럼명 조회하기
    colname = cursor.description
    
    ### {} 형태로 변환
    dict_col = getFetchAll(colname, rows)
    
    ### DB연결 해제하기
    DBClose(cursor, conn)
    
    return dict_col

