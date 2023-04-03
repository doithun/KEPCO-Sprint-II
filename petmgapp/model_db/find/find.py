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

### 찾고있어요 내역 삭제(조건: 본인이 작성한 게시물만 삭제가능)
def FindDelete(req_no, f_mem_id) :

    conn, cursor = getDBConn_Cursor()
        
    try:         
            
        ### SQL 구문 작성
        sql = """
                DELETE FROM DOG_FIND WHERE req_no = {} and f_mem_id = '{}'
        """.format(req_no, f_mem_id)
        
        cursor.execute(sql)
        
        conn.commit()
    except:    
        DBClose(cursor, conn)
        return "no"

    DBClose(cursor, conn)
    return "ok"


def FindUpdate(data) :
    conn, cursor = getDBConn_Cursor()
        
    try:         
            
        ### SQL 구문 작성
        sql = """
        
        UPDATE DOG_FIND SET sexcd = '{2}', popfile='{3}', processstate='{4}', happendt='{5}', happenplace='{6}', kindcd='{7}', colorcd='{8}', age='{9}', neuteryn='{10}', specialmark='{11}'
                        WHERE req_no = {0} and f_mem_id = '{1}'
        """.format(data['req_no'],data['f_mem_id'],data['sexcd'],data['popfile'],data['processstate'],data['happendt'],data['happenplace'],data['kindcd']
                    ,data['colorcd'],data['age'],data['neuteryn'],data['specialmark'])

        cursor.execute(sql)
        
        conn.commit()
    except:    
        DBClose(cursor, conn)
        return "no"

    DBClose(cursor, conn)
    return "ok"
    # conn, cursor = getDBConn_Cursor()
    
    # try:         
    #     # popfile = data['popfile']
        
    #     # if  popfile != '':
    #     #     ### SQL 구문 작성
    #     #     sql = """
            
    #     #     UPDATE DOG_FIND SET sexcd = '{2}', popfile='{3}', processstate='{4}', happendt='{5}', happenplace='{6}', kindcd='{7}', colorcd='{8}', age='{9}', neuteryn='{10}', specialmark='{11}'
    #     #                     WHERE req_no = {0} and f_mem_id = '{1}'
    #     #     """.format(data['req_no'],data['f_mem_id'],data['sexcd'],data['popfile'],data['processstate'],data['happendt'],data['happenplace'],data['kindcd']
    #     #                 ,data['colorcd'],data['age'],data['neuteryn'],data['specialmark'])
    #     # else : 
            
    #     #     sql = """
    #     #         Select popfile From DOG_FIND
    #     #             where req_no =: req_no 
    #     #                 And f_mem_id =: f_mem_id
    #     #     """
    #     #     cursor.execute(sql, req_no=data['req_no'], f_mem_id=data['f_mem_id'])
                
    #     #     row = cursor.fetchone()
            
    #     #     data['popfile'] = row[0]
        
    #     ### SQL 구문 작성
    #     sql = """
        
    #     UPDATE DOG_FIND SET sexcd = '{2}', popfile='{3}', processstate='{4}', happendt='{5}', happenplace='{6}', kindcd='{7}', colorcd='{8}', age='{9}', neuteryn='{10}', specialmark='{11}'
    #                     WHERE req_no = {0} and f_mem_id = '{1}'
    #     """.format(data['req_no'],data['f_mem_id'],data['sexcd'],data['popfile'],data['processstate'],data['happendt'],data['happenplace'],data['kindcd']
    #                 ,data['colorcd'],data['age'],data['neuteryn'],data['specialmark'])            

    #     cursor.execute(sql)
        
    #     conn.commit()
    # except:    
    #     DBClose(cursor, conn)
    #     return "no"

    # DBClose(cursor, conn)
    # return "ok"


### 한건 조회
def FindUpdateView(req_no, f_mem_id) :
    ### DB접속하기
    conn, cursor = getDBConn_Cursor()
    
    sql = """
            Select * From DOG_FIND
                where req_no =: req_no 
                    And f_mem_id =: f_mem_id
    """
    cursor.execute(sql, req_no=req_no, f_mem_id=f_mem_id)
    
    rows = cursor.fetchone()
    
    ### 컬럼명 조회하기
    colname = cursor.description  
    
    ### {}형태로 변환
    dict_col = getFetchOne(colname, rows)
    
    ### DB연결 해제하기
    DBClose(cursor, conn)
    
    return dict_col

#####################  find  #####################
def getFind() :
    conn, cursor = getDBConn_Cursor()
    
    ### SQL 구문 작성
    sql = """
            select *  
                from dog_find a
                    left join member b on b.mem_id = a.f_mem_id
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

def getFindView(req_no, f_mem_id) :
    conn, cursor = getDBConn_Cursor()
    
    ### SQL 구문 작성
    sql = """
            select *  
                from dog_find a
                    left join member b on b.mem_id = a.f_mem_id
                        where req_no =: req_no and f_mem_id =: f_mem_id
    """
    ### 구문을 서버에게 보내서 요청하고, 결과 받아오기
    cursor.execute(sql, req_no = req_no, f_mem_id = f_mem_id)
    
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

def getFindSearch(s_table, s_col, keyword) :
    conn, cursor = getDBConn_Cursor()
    
    sql = """
            select * from {} a
            left join member b on b.mem_id = a.f_mem_id
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