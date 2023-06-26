from django.shortcuts import render
from django.http import HttpResponse

###회원관리
import petmgapp.model_db.member.member as mem

###후원신청
import petmgapp.model_db.support.support as support

###신고할래요
import petmgapp.model_db.report.report as report

###찾고있어요 
import petmgapp.model_db.find.find as find

###발견했어요
import petmgapp.model_db.notice.notice as notice

###보호중이에요
import petmgapp.model_db.protect.protect as protect

###파일 업로드, 내려받기 라이브러리
from petmgapp.model_db.file_util.file_util import File_Util

### 페이징처리 라이브러리
from django.core.paginator import Paginator

### 카카오 지도 api 라이브러리
import petmgapp.model_db.api.kakao_api as kakao

# Create your views here.

### 인트로
def getIntro(request) : 
    return render(request,
                    "petmgapp/intro/intro.html",
                        {})
    
### 메인    
def getBase(request) : 
    return render(request,
                    "petmgapp/base.html",
                        {})
        
def getReport(request) : 
    # if request.session.get("ses_mem_id") :
        return render(request,
                        "petmgapp/report/report.html",
                            {})
    # else :
    #     msg="""
    #         <script type='text/javascript'>
    #             alert('잘못된 접근입니다. 로그인하세요!!!');
    #             location.href ='/pet/login_logout/;
    #         </script>
    #     """
    #     return HttpResponse(msg)       
        

###신고할래요(실종, 구조, 목격)
def ReportInsert(request) :
        try:
            if request.FILES['popfile'] :
                popfile = request.FILES['popfile']
        except:
            msg = """
                    <script type='text/javascript'>
                        alert('잘못된 접근입니다. 다시 입력하세요!');
                        location.href = '/pet/report_view/'
                    </script>
            """
            return HttpResponse(msg)
    
        ############################################
        #############[파일 업로드 처리]###############
        ### 파일 업로드 폴더 위치 지정
        upload_dir = "./petmgapp/static/petmgapp/file_manager/"
        
        ### 파일 다운로드 폴더 위치 지정
        down_dir = "/static/petmgapp/file_manager/"
        
        ### 파일 처리를 위한 클래스 생성 
        fu = File_Util()
        fu.setUpload(popfile, upload_dir, down_dir)
        fu.fileUpload()
        
        ### 파일사이즈
        file_size = fu.file_size
        
        ### 다운로드 파일명(경로 + 파일명) 
        file_full_name = fu.file_full_name
        
        ### 다운로드를 위해 DB의 파일명만 추출하기
        # /static/nonmodelapp/file_manager/dog01_aU2bFG7.jpg을 
        # "/" 기호로 split한 후 마지막 위치의 index번호 값 추출
        filename = file_full_name.split("/")[-1]
        
        ### 다운로드를 위한 파일명(전체경로 + 파일명)
        downFullName = "/static/petmgapp/file_manager/"+filename
            
        ### 테이블에 입력 시 아래처럼 파일명 처리
        # 사용하시는 테이블 내에 컬럼명이 downFullName 이라고 한다면...
        # "Insert into 테이블명 (컬럼명1, 컬럼명2, downFullName) 
        #     values({}, {}, '{}')".format(값1, 값2, downFullName) 
        ######################################### 

        try:
                ### 사용자가 입력한 값들 추출하기
                ### get 방식 처리
            if request.method == "GET" :
                    processstate = request.GET.get("processstate","") 
                    happendt = request.GET.get("happendt","")  
                    happenplace = request.GET.get("happenplace","") 
                    kindcd = request.GET.get("kindcd","") 
                    colorcd = request.GET.get("colorcd","") 
                    age = request.GET.get("age","")  
                    sexcd = request.GET.get("sexcd","") 
                    neuteryn = request.GET.get("neuteryn","") 
                    specialmark = request.GET.get("specialmark","") 

            ### post 방식 처리
            elif request.method == "POST" :
                    processstate = request.POST.get("processstate","") 
                    happendt = request.POST.get("happendt","")  
                    happenplace = request.POST.get("happenplace","") 
                    kindcd = request.POST.get("kindcd","") 
                    colorcd = request.POST.get("colorcd","") 
                    age = request.POST.get("age","")  
                    sexcd = request.POST.get("sexcd","") 
                    neuteryn = request.POST.get("neuteryn","") 
                    specialmark = request.POST.get("specialmark","") 
                    

            data = {
                    'f_mem_id' : request.session["ses_mem_id"],
                    'popfile' : downFullName,
                    'processstate': processstate, 
                    'happendt': happendt,
                    'happenplace': happenplace,
                    'kindcd': kindcd,
                    'colorcd': colorcd,
                    'age': age,
                    'sexcd': sexcd,
                    'neuteryn': neuteryn,
                    'specialmark': specialmark
                    }    
            
            report.ReportCreate(data)
                
                # return HttpResponse(data["processstate"])
                # return HttpResponse(data["happendt"])
                # return HttpResponse(data["happenplace"])
                # return HttpResponse(data["kindcd"])
                # return HttpResponse(data["colorcd"])
                # return HttpResponse(data["age"])
                # return HttpResponse(data["sexcd"])
                # return HttpResponse(data["neuteryn"])
                # return HttpResponse(data["specialmark"])
                                            
        except:
                msg = """
                        <script type='text/javascript'>
                                alert('저장중 에러가 발생하였습니다!');
                                history.go(-1);
                        </script>
                """
                return HttpResponse(msg)
            
        ### 저장 잘되었다는 창 띄우고,
        #   - 원래 페이지로 가기..
        url = "/pet/find/"
    
        msg = """
        <script type='text/javascript'>
            alert('접수 되었습니다!');
            location.href = '{}';
        </script>
        """.format(url)  
        
        return HttpResponse(msg)
########################################

### TIP
def getTip1(request) : 
    return render(request,
                    "petmgapp/tip/tip01.html",
                        {})
    
def getTip2(request) : 
    return render(request,
                    "petmgapp/tip/tip02.html",
                        {})
    
def getTip3(request) : 
    return render(request,
                    "petmgapp/tip/tip03.html",
                        {})

    

#####################################################
###회원관리
#####################################################
def getMemberInsert(request):
    return render(request,
                "petmgapp/login/mem_insert.html")
    
    
    
##로그인
def MemberInsert(request):
    
    if request.method == "POST" :
        mem_id =request.POST["mem_id"]
        mem_pass =request.POST["mem_pass"]
        mem_name=request.POST["mem_name"]
        mem_email=request.POST["mem_email"]
    elif request.method == "GET" :
        mem_id =request.GET["mem_id"]
        mem_pass =request.GET["mem_pass"]
        mem_name=request.GET["mem_name"]
        mem_email=request.GET["mem_email"]
    
    rs = mem.MemberInsert(mem_id, mem_pass, mem_name, mem_email )

    if mem_id == '' :
        msg="""
            <script type='text/javascript'>
                alert('아이디는 필수입력사항 입니다.');
                history.go(-1);
            </script>
        """
        return HttpResponse(msg) 
    
    if mem_pass == '':
        msg="""
            <script type='text/javascript'>
                alert('비밀번호는 필수입력사항 입니다.');
                history.go(-1);
            </script>
        """        
        return HttpResponse(msg) 
    
    if mem_name == '':
        msg="""
            <script type='text/javascript'>
                alert('이름은 필수입력사항 입니다.');
                history.go(-1);
            </script>
        """    
        return HttpResponse(msg) 

    if mem_email == '':
        msg="""
            <script type='text/javascript'>
                alert('이메일은 필수입력사항 입니다.');
                history.go(-1);
            </script>
        """               
        return HttpResponse(msg)        
    
    if rs=='no':
        msg="""
            <script type='text/javascript'>
                alert('아이디 비밀번호를 확인하세요.');
                history.go(-1);
            </script>
        """
        return HttpResponse(msg)
    
    else :   
        msg="""
            <script type='text/javascript'>
                alert('회원가입이 완료되었습니다.');
                location.href='/pet/login_logout/';
            </script>
        """
        return HttpResponse(msg)

def getDelete(request):
    return render(request,
                "petmgapp/login/mem_delete.html")

def MemberDelete(request):
    if request.method == "POST" :
        mem_id =request.POST["mem_id"]
        mem_pass =request.POST["mem_pass"]
        mem_name=request.POST["mem_name"]
        mem_email=request.POST["mem_email"]
        
    elif request.method == "GET" :
        mem_id =request.GET["mem_id"]
        mem_pass =request.GET["mem_pass"]
        mem_name=request.GET["mem_name"]
        mem_email=request.GET["mem_email"]
        
    
    rs = mem.MemberDelete(mem_id, mem_pass, mem_name, mem_email )
    
    
    if rs=='no':
        msg="""
            <script type='text/javascript'>
                alert('없는계정입니다');
                history.go(-1);
            </script>
        """
        return HttpResponse(msg)
        
    msg="""
        <script type='text/javascript'>
            alert('회원탈퇴가 완료되었습니다.');
            location.href='/pet/login_logout/';
        </script>
    """
    return HttpResponse(msg)

def MemberUpdate(request):
    if request.method == "POST" :
        mem_id =request.POST["mem_id"]
        mem_pass =request.POST["mem_pass"]
        mem_name=request.POST["mem_name"]
        mem_email=request.POST["mem_email"]
        
    elif request.method == "GET" :
        mem_id =request.GET["mem_id"]
        mem_pass =request.GET["mem_pass"]
        mem_name=request.GET["mem_name"]
        mem_email=request.GET["mem_email"]
        
    if mem_pass == '' :
        msg="""
            <script type='text/javascript'>
                alert('변경하실 비밀번호를 입력 해주세요.');
                history.go(-1);
            </script>
        """
        return HttpResponse(msg) 

    if mem_email == '' :
        msg="""
            <script type='text/javascript'>
                alert('변경하실 이메일 주소를 입력 해주세요.');
                history.go(-1);
            </script>
        """
        return HttpResponse(msg) 
    
    rs,sql = mem.MemberUpdate(mem_id, mem_pass, mem_name, mem_email )

    if rs=='no':
        msg="""
            <script type='text/javascript'>
                alert('오류입니다');
                history.go(-1);
            </script>
        """
        return HttpResponse(msg)
        
    msg="""
        <script type='text/javascript'>
            alert('회원정보가 저장되었습니다. 다시 로그인 해주세요.');
            location.href ='/pet/logout/';
        </script>
    """
    return HttpResponse(msg)

################################################################################################

def login_logout(request):
    return render(request,
                "petmgapp/login/login_logout.html",
                {})
    
def login(request):
    try :
        if request.method == "POST" :
            mem_id = request.POST["mem_id"]
            mem_pass = request.POST["mem_pass"]
                    
        elif request.method == "GET" :        
            mem_id = request.GET["mem_id"]
            mem_pass = request.GET["mem_pass"]
            
    except :
        url = "/pet/login_logout/"

        msg="""
            <script type='text/javascript'>
                alert('잘못된 접근입니다. 로그인하세요');
                location.href ='{}';
            </script>
        """.format(url) 

        return HttpResponse(msg)
    
    ## DB
    dict_col = mem.getLogin(mem_id, mem_pass)
# return HttpResponse(dict_col["rs"])
    # return HttpResponse(mem_pass)
    
    ### 성공여부
    if dict_col["rs"] == "no" :
        msg="""
            <script type="text/javascript">
                alert('아이디 또는 비밀번호가 일치하지 않습니다.');
                history.go(-1);
            </script>
        """
        
        return HttpResponse(msg)
        
    request.session["ses_mem_id"]=mem_id
    request.session["ses_mem_name"] = dict_col["mem_name"]
    
    return render(request,
                "petmgapp/base.html",
                    {})
    
def logout(request):
    if request.session.get("ses_mem_id"):
        ### 세션 정보 비우기
        request.session.flush()
        
        msg="""
            <script type='text/javascript'>
                alert('로그아웃 되었습니다.');
                location.href ='/index';
            </script>
        """
    else :
        msg="""
            <script type='text/javascript'>
                alert('잘못된 접근입니다. 로그인하세요!!!');
                location.href ='/index';
            </script>
        """
    return HttpResponse(msg)

def getMember(request):
    try :
        dict_col = mem.getMember(request.session["ses_mem_id"])
                
    except :
        url = "/pet/login_logout/"

        msg="""
            <script type='text/javascript'>
                alert('잘못된 접근입니다. 로그인하세요');
                location.href ='{}';
            </script>
        """.format(url) 

        return HttpResponse(msg)
    
    return render(request,
            "petmgapp/login/mem_my.html",
            {"dict_col":dict_col})
############################################   요기!     ############################################################

def getNotice(request) : 
    ### 현재 선택된 페이지 데이터 받아오기
    # - 최초에는 GET방식으로 넘어오는 데이터가 없음
    #   -> get("page","1") : 데이터가 없으면 1로 초기화 시킴
    now_page = request.GET.get("page","1")
    
    #return HttpResponse(now_page)
    
    try:
        ### request로 넘어오는 모든 데이터는
        # --> 문자열 데이터임
        # --> 페이지번호는 숫자형태를 사용해야함
        #     (형변환 시켜야 함)
        now_page = request.GET.get("page","1")
        now_page = int(now_page)
    except:
        now_page = 1
        
    ### 데이터 조회
    dog_list = notice.getNotice()
    ########################################
    ### 페이징 처리 : 페이지 번호의 범위 계산
    # 1 ~ 10
    
    ### 한 페이지에 보여줄 행의 갯수 지정
    num_row = 10
    ### 페이징 처리 라이브러리에
    # - DB에서 조회한 데이터 전체와
    # - 한 페이지에 보여줄 행의 갯수 변수를 넘깁니다.
    p = Paginator(dog_list, num_row)
    
    ### 현재 선택된 페이지번호(now_page)에 해당하는 
    # - 10개의 행을 추출하기
    rows_data = p.get_page(now_page)
    
    ### 게시물 하단에 표시할 시작 페이지번호 계산하기
    start_page = (now_page -1) // num_row * num_row + 1
    
    ### 계시물 하단에 표시할 마지막 페이지번호 계산하기
    end_page = start_page + 9
    
    ### 마지막 페이지번호 처리하기
    # p.num_pages : pagenator가 관리하는 전체 페이지 번호
    if end_page > p.num_pages : 
        end_page = p.num_pages
        
    ########################################
    ### 페이징 처리 : 다음 / 이전 버튼 처리하기
    
    ### 이전(is_prev), 다음(is_ next) 버튼을 보여줄지 여부를
    #   - 저장할 boolean 변수
    is_prev = False
    is_next = False
    
    ### 시작 페이지 번호(start_page)가 1보다 크면
    # - 이전 버튼을 보이게 하기 위해 True값으로 변경
    if start_page > 1 :
        is_prev = True
        
    ### 종료 페이지 번호(end_page)가
    # - 전체 페이지 번호(p.num_pages)보다 작으면
    # - 다음 버튼을 보이기
    if end_page < p.num_pages :
        is_next = True
        
    context = {
        "rows_data" : rows_data,
        "is_prev" : is_prev,
        "is_next" : is_next,
        "start_page" : start_page,
        "page_range" : range(start_page, end_page + 1),
    }
    
    return render(request,
                    "petmgapp/notice/notice.html",
                        context)
    
def getNoticeView(request) : 
    if request.method == "GET" :
        desertionno = request.GET["desertionno"]
        s_table = request.GET["s_table"]
    elif request.method == "POST" :
        desertionno = request.POST["desertionno"]
        s_table = request.GET["s_table"]
    
    # return HttpResponse(s_table)
        
    dog_list = notice.getNoticeView(desertionno, s_table)
    
    location = [dog_list['careaddr']]
    
    # return HttpResponse(location)
    if kakao.getLocation_info(location) != False:
        df, x, y = kakao.getLocation_info(location)
    else :
        return render(request,
                        "petmgapp/notice/notice_view.html",
                            {"dog_list" : dog_list,
                            "s_table" : s_table,
                            "location_map" : ""})       
    
    location_xy = [x,y]
    
    location_map = kakao.getKakaoMapHtml(dog_list['carenm'],y, x)
    
    # return HttpResponse(location_map)

    return render(request,
                    "petmgapp/notice/notice_view.html",
                        {"dog_list" : dog_list,
                        "s_table" : s_table,
                        "location_map" : location_map})

#############################   protect    ##################################
def getProtect(request) : 
    ### 현재 선택된 페이지 데이터 받아오기
    # - 최초에는 GET방식으로 넘어오는 데이터가 없음
    #   -> get("page","1") : 데이터가 없으면 1로 초기화 시킴
    now_page = request.GET.get("page","1")
    
    try:
        ### request로 넘어오는 모든 데이터는
        # --> 문자열 데이터임
        # --> 페이지번호는 숫자형태를 사용해야함
        #     (형변환 시켜야 함)
        now_page = request.GET.get("page","1")
        now_page = int(now_page)
    except:
        now_page = 1
        
    ### 데이터 조회
    dog_list = protect.getProtect()
    ########################################
    ### 페이징 처리 : 페이지 번호의 범위 계산
    # 1 ~ 10
    
    ### 한 페이지에 보여줄 행의 갯수 지정
    num_row = 10
    ### 페이징 처리 라이브러리에
    # - DB에서 조회한 데이터 전체와
    # - 한 페이지에 보여줄 행의 갯수 변수를 넘깁니다.
    p = Paginator(dog_list, num_row)
    
    ### 현재 선택된 페이지번호(now_page)에 해당하는 
    # - 10개의 행을 추출하기
    rows_data = p.get_page(now_page)
    
    ### 게시물 하단에 표시할 시작 페이지번호 계산하기
    start_page = (now_page -1) // num_row * num_row + 1
    
    ### 계시물 하단에 표시할 마지막 페이지번호 계산하기
    end_page = start_page + 9
    
    ### 마지막 페이지번호 처리하기
    # p.num_pages : pagenator가 관리하는 전체 페이지 번호
    if end_page > p.num_pages : 
        end_page = p.num_pages
        
    ########################################
    ### 페이징 처리 : 다음 / 이전 버튼 처리하기
    
    ### 이전(is_prev), 다음(is_ next) 버튼을 보여줄지 여부를
    #   - 저장할 boolean 변수
    is_prev = False
    is_next = False
    
    ### 시작 페이지 번호(start_page)가 1보다 크면
    # - 이전 버튼을 보이게 하기 위해 True값으로 변경
    if start_page > 1 :
        is_prev = True
        
    ### 종료 페이지 번호(end_page)가
    # - 전체 페이지 번호(p.num_pages)보다 작으면
    # - 다음 버튼을 보이기
    if end_page < p.num_pages :
        is_next = True
        
    context = {
        "rows_data" : rows_data,
        "is_prev" : is_prev,
        "is_next" : is_next,
        "start_page" : start_page,
        "page_range" : range(start_page, end_page + 1),
    }
    return render(request,
                    "petmgapp/protect/protect.html",
                        context)
    
def getProtectView(request) : 
    if request.method == "GET" :
        desertionno = request.GET["desertionno"]
        s_table = request.GET["s_table"]
    elif request.method == "POST" :
        desertionno = request.POST["desertionno"]
        s_table = request.GET["s_table"]
    
    # return HttpResponse(s_table)
        
    dog_list = protect.getProtectView(desertionno, s_table)

    location = [dog_list['careaddr']]
    
    # return HttpResponse(location)
    if kakao.getLocation_info(location) != False:
        df, x, y = kakao.getLocation_info(location)
    else :
        return render(request,
                        "petmgapp/notice/notice_view.html",
                            {"dog_list" : dog_list,
                            "s_table" : s_table,
                            "location_map" : ""})       
    
    location_xy = [x,y]
    
    location_map = kakao.getKakaoMapHtml(dog_list['carenm'],y, x)
    
    # return HttpResponse(location_map)
        
    return render(request,
                    "petmgapp/protect/protect_view.html",
                        {"dog_list" : dog_list,
                        "s_table" : s_table,
                        "location_map" : location_map})


def getFind(request) : 
    ### 현재 선택된 페이지 데이터 받아오기
    # - 최초에는 GET방식으로 넘어오는 데이터가 없음
    #   -> get("page","1") : 데이터가 없으면 1로 초기화 시킴
    now_page = request.GET.get("page","1")
    
    #return HttpResponse(now_page)
    
    try:
        ### request로 넘어오는 모든 데이터는
        # --> 문자열 데이터임
        # --> 페이지번호는 숫자형태를 사용해야함
        #     (형변환 시켜야 함)
        now_page = request.GET.get("page","1")
        now_page = int(now_page)
    except:
        now_page = 1
        
    ### 데이터 조회
    dog_list = find.getFind()
    #return HttpResponse(dog_list)
    ########################################
    ### 페이징 처리 : 페이지 번호의 범위 계산
    # 1 ~ 10
    
    ### 한 페이지에 보여줄 행의 갯수 지정
    num_row = 10
    ### 페이징 처리 라이브러리에
    # - DB에서 조회한 데이터 전체와
    # - 한 페이지에 보여줄 행의 갯수 변수를 넘깁니다.
    p = Paginator(dog_list, num_row)
    
    ### 현재 선택된 페이지번호(now_page)에 해당하는 
    # - 10개의 행을 추출하기
    rows_data = p.get_page(now_page)
    
    ### 게시물 하단에 표시할 시작 페이지번호 계산하기
    start_page = (now_page -1) // num_row * num_row + 1
    
    ### 계시물 하단에 표시할 마지막 페이지번호 계산하기
    end_page = start_page + 9
    
    ### 마지막 페이지번호 처리하기
    # p.num_pages : pagenator가 관리하는 전체 페이지 번호
    if end_page > p.num_pages : 
        end_page = p.num_pages
        
    ########################################
    ### 페이징 처리 : 다음 / 이전 버튼 처리하기
    
    ### 이전(is_prev), 다음(is_ next) 버튼을 보여줄지 여부를
    #   - 저장할 boolean 변수
    is_prev = False
    is_next = False
    
    ### 시작 페이지 번호(start_page)가 1보다 크면
    # - 이전 버튼을 보이게 하기 위해 True값으로 변경
    if start_page > 1 :
        is_prev = True
        
    ### 종료 페이지 번호(end_page)가
    # - 전체 페이지 번호(p.num_pages)보다 작으면
    # - 다음 버튼을 보이기
    if end_page < p.num_pages :
        is_next = True
        
    context = {
        "rows_data" : rows_data,
        "is_prev" : is_prev,
        "is_next" : is_next,
        "start_page" : start_page,
        "page_range" : range(start_page, end_page + 1),
    }
    
    return render(request,
                    "petmgapp/find/find.html",
                        context)
    
def getFindView(request) : 
    if request.method == "GET" :
        req_no = request.GET["req_no"]
        f_mem_id = request.GET["f_mem_id"]
        
    elif request.method == "POST" :
        req_no = request.POST["req_no"]
        f_mem_id = request.GET["f_mem_id"]
        
    dog_list = find.getFindView(req_no, f_mem_id)
    return render(request,
                    "petmgapp/find/find_view.html",
                        {"dog_list" : dog_list})

def getFindSearch(request) : 
    
    if request.method == "GET" :
                s_table = request.GET["s_table"]
                s_col = request.GET["s_col"]   
                keyword = request.GET["keyword"]   
        ### post 방식 처리
    elif request.method == "POST" :
            s_table = request.POST["s_table"]
            s_col = request.POST["s_col"]  
            keyword = request.POST["keyword"]  
            
    ### 현재 선택된 페이지 데이터 받아오기
    # - 최초에는 GET방식으로 넘어오는 데이터가 없음
    #   -> get("page","1") : 데이터가 없으면 1로 초기화 시킴
    now_page = request.GET.get("page","1")
    #return HttpResponse(now_page)
    
    try:
        ### request로 넘어오는 모든 데이터는
        # --> 문자열 데이터임
        # --> 페이지번호는 숫자형태를 사용해야함
        #     (형변환 시켜야 함)
        now_page = request.GET.get("page","1")
        now_page = int(now_page)
    except:
        now_page = 1
        
        
    temp_keyword = s_col
    temp_keyword2 = keyword        
    
    # return HttpResponse(s_col)

    ### 데이터 조회
    dog_list = find.getFindSearch(s_table, s_col, keyword)
    

    ########################################
    ### 페이징 처리 : 페이지 번호의 범위 계산
    # 1 ~ 10
    
    ### 한 페이지에 보여줄 행의 갯수 지정
    num_row = 10
    ### 페이징 처리 라이브러리에
    # - DB에서 조회한 데이터 전체와
    # - 한 페이지에 보여줄 행의 갯수 변수를 넘깁니다.
    p = Paginator(dog_list, num_row)
    
    ### 현재 선택된 페이지번호(now_page)에 해당하는 
    # - 10개의 행을 추출하기
    rows_data = p.get_page(now_page)
    
    ### 게시물 하단에 표시할 시작 페이지번호 계산하기
    start_page = (now_page -1) // num_row * num_row + 1
    
    ### 계시물 하단에 표시할 마지막 페이지번호 계산하기
    end_page = start_page + 9
    
    ### 마지막 페이지번호 처리하기
    # p.num_pages : pagenator가 관리하는 전체 페이지 번호
    if end_page > p.num_pages : 
        end_page = p.num_pages
        
    ########################################
    ### 페이징 처리 : 다음 / 이전 버튼 처리하기
    
    ### 이전(is_prev), 다음(is_ next) 버튼을 보여줄지 여부를
    #   - 저장할 boolean 변수
    is_prev = False
    is_next = False
    
    ### 시작 페이지 번호(start_page)가 1보다 크면
    # - 이전 버튼을 보이게 하기 위해 True값으로 변경
    if start_page > 1 :
        is_prev = True
        
    ### 종료 페이지 번호(end_page)가
    # - 전체 페이지 번호(p.num_pages)보다 작으면
    # - 다음 버튼을 보이기
    if end_page < p.num_pages :
        is_next = True
        
    context = {
        "rows_data" : rows_data,
        "is_prev" : is_prev,
        "is_next" : is_next,
        "start_page" : start_page,
        "page_range" : range(start_page, end_page + 1),
        "temp_keyword" : temp_keyword,
        "temp_keyword2" : temp_keyword2
    }
    return render(request,"petmgapp/find/find_search.html",context)

def getNoticeSearch(request) : 
    
    if request.method == "GET" :
                s_table = request.GET["s_table"]
                s_col = request.GET["s_col"]   
                keyword = request.GET["keyword"]   
        ### post 방식 처리
    elif request.method == "POST" :
            s_table = request.POST["s_table"]
            s_col = request.POST["s_col"]  
            keyword = request.POST["keyword"]  
            
    temp1 = s_table
    temp2 = s_col
    temp3 = keyword  

    #return HttpResponse(temp1)

    ### 현재 선택된 페이지 데이터 받아오기
    # - 최초에는 GET방식으로 넘어오는 데이터가 없음
    #   -> get("page","1") : 데이터가 없으면 1로 초기화 시킴
    now_page = request.GET.get("page","1")
    
    #return HttpResponse(now_page)
    
    try:
        ### request로 넘어오는 모든 데이터는
        # --> 문자열 데이터임
        # --> 페이지번호는 숫자형태를 사용해야함
        #     (형변환 시켜야 함)
        now_page = request.GET.get("page","1")
        now_page = int(now_page)
    except:
        now_page = 1
        
    ### 데이터 조회
    dog_list = notice.getNoitceSearch(s_table, s_col, keyword)
    ########################################
    ### 페이징 처리 : 페이지 번호의 범위 계산
    # 1 ~ 10
    
    ### 한 페이지에 보여줄 행의 갯수 지정
    num_row = 10
    ### 페이징 처리 라이브러리에
    # - DB에서 조회한 데이터 전체와
    # - 한 페이지에 보여줄 행의 갯수 변수를 넘깁니다.
    p = Paginator(dog_list, num_row)
    
    ### 현재 선택된 페이지번호(now_page)에 해당하는 
    # - 10개의 행을 추출하기
    rows_data = p.get_page(now_page)
    
    ### 게시물 하단에 표시할 시작 페이지번호 계산하기
    start_page = (now_page -1) // num_row * num_row + 1
    
    ### 계시물 하단에 표시할 마지막 페이지번호 계산하기
    end_page = start_page + 9
    
    ### 마지막 페이지번호 처리하기
    # p.num_pages : pagenator가 관리하는 전체 페이지 번호
    if end_page > p.num_pages : 
        end_page = p.num_pages
        
    ########################################
    ### 페이징 처리 : 다음 / 이전 버튼 처리하기
    
    ### 이전(is_prev), 다음(is_ next) 버튼을 보여줄지 여부를
    #   - 저장할 boolean 변수
    is_prev = False
    is_next = False
    
    ### 시작 페이지 번호(start_page)가 1보다 크면
    # - 이전 버튼을 보이게 하기 위해 True값으로 변경
    if start_page > 1 :
        is_prev = True
        
    ### 종료 페이지 번호(end_page)가
    # - 전체 페이지 번호(p.num_pages)보다 작으면
    # - 다음 버튼을 보이기
    if end_page < p.num_pages :
        is_next = True
        
    context = {
        "rows_data" : rows_data,
        "is_prev" : is_prev,
        "is_next" : is_next,
        "start_page" : start_page,
        "page_range" : range(start_page, end_page + 1),
        "temp1" : temp1,
        "temp2" : temp2,
        "temp3" : temp3
    }
    
    return render(request,
                    "petmgapp/notice/notice_search.html",
                        context)

def getProtectSearch(request) : 
    
    if request.method == "GET" :
                s_table = request.GET["s_table"]
                s_col = request.GET["s_col"]   
                keyword = request.GET["keyword"]   
        ### post 방식 처리
    elif request.method == "POST" :
            s_table = request.POST["s_table"]
            s_col = request.POST["s_col"]  
            keyword = request.POST["keyword"]  
            
    temp1 = s_table
    temp2 = s_col
    temp3 = keyword 
                
    ### 현재 선택된 페이지 데이터 받아오기
    # - 최초에는 GET방식으로 넘어오는 데이터가 없음
    #   -> get("page","1") : 데이터가 없으면 1로 초기화 시킴
    now_page = request.GET.get("page","1")
    
    try:
        ### request로 넘어오는 모든 데이터는
        # --> 문자열 데이터임
        # --> 페이지번호는 숫자형태를 사용해야함
        #     (형변환 시켜야 함)
        now_page = request.GET.get("page","1")
        now_page = int(now_page)
    except:
        now_page = 1
        

    ### 데이터 조회
    dog_list = protect.getProtectSearch(s_table, s_col, keyword)
    

    ########################################
    ### 페이징 처리 : 페이지 번호의 범위 계산
    # 1 ~ 10
    
    ### 한 페이지에 보여줄 행의 갯수 지정
    num_row = 10
    ### 페이징 처리 라이브러리에
    # - DB에서 조회한 데이터 전체와
    # - 한 페이지에 보여줄 행의 갯수 변수를 넘깁니다.
    p = Paginator(dog_list, num_row)
    
    ### 현재 선택된 페이지번호(now_page)에 해당하는 
    # - 10개의 행을 추출하기
    rows_data = p.get_page(now_page)
    
    ### 게시물 하단에 표시할 시작 페이지번호 계산하기
    start_page = (now_page -1) // num_row * num_row + 1
    
    ### 계시물 하단에 표시할 마지막 페이지번호 계산하기
    end_page = start_page + 9
    
    ### 마지막 페이지번호 처리하기
    # p.num_pages : pagenator가 관리하는 전체 페이지 번호
    if end_page > p.num_pages : 
        end_page = p.num_pages
        
    ########################################
    ### 페이징 처리 : 다음 / 이전 버튼 처리하기
    
    ### 이전(is_prev), 다음(is_ next) 버튼을 보여줄지 여부를
    #   - 저장할 boolean 변수
    is_prev = False
    is_next = False
    
    ### 시작 페이지 번호(start_page)가 1보다 크면
    # - 이전 버튼을 보이게 하기 위해 True값으로 변경
    if start_page > 1 :
        is_prev = True
        
    ### 종료 페이지 번호(end_page)가
    # - 전체 페이지 번호(p.num_pages)보다 작으면
    # - 다음 버튼을 보이기
    if end_page < p.num_pages :
        is_next = True
        
    context = {
        "rows_data" : rows_data,
        "is_prev" : is_prev,
        "is_next" : is_next,
        "start_page" : start_page,
        "page_range" : range(start_page, end_page + 1),
        "temp1" : temp1,
        "temp2" : temp2,
        "temp3" : temp3
    }
    return render(request,"petmgapp/protect/protect_search.html",context)


######################## support #####################################
def getSupport(request):
    if request.method == "GET" :
        desertionno = request.GET["desertionno"]
        s_table = request.GET["s_table"]
    elif request.method == "POST" :
        desertionno = request.POST["desertionno"]
        s_table = request.GET["s_table"]
        
    # return HttpResponse(s_table)
            
    dog_list = support.getSupport(desertionno, s_table)
    
    return render(request,
                    "petmgapp/support/support.html",
                        {"dog_list":dog_list})

def SupportInsert(request):
    if request.method == "GET" :
        desertionno = request.GET["desertionno"]
        support_type = request.GET["support_type"]
        money = request.GET["money"]
        
    elif request.method == "POST" :
        desertionno = request.POST.get("desertionno")
        support_type = request.POST["support_type"]
        money = request.POST["money"]
            
    # return HttpResponse(money)

    support.SupportInsert(request.session["ses_mem_id"], desertionno, support_type, money)

    msg="""
            <script type='text/javascript'>
                alert('후원이 성공적으로 신청되었습니다.');
                location.href='/pet/support_list/';
            </script>
        """.format(desertionno)
        
    return HttpResponse(msg)


def getSupportView(request) : 
    if request.method == "GET" :
        desertionno = request.GET["desertionno"]
    elif request.method == "POST" :
        desertionno = request.POST["desertionno"]
    dog_list = support.getSupportView(desertionno)
    return render(request,
                    "petmgapp/support/support_view.html",
                    {"dog_list" : dog_list})
    
    
def FindDelete(request) :
    try:
        if request.method == "GET" :
            req_no = request.GET["req_no"]
            f_mem_id = request.GET["f_mem_id"]
        elif request.method == "POST" :
            req_no = request.POST["req_no"]
            f_mem_id = request.POST["f_mem_id"]
            
        find.FindDelete(req_no, f_mem_id)
    except:
        msg = """
                <script type='text/javascript'>
                        alert('삭제중 에러가 발생하였습니다!');
                        history.go(-1);
                </script>
        """
        return HttpResponse(msg)
    
    ### 삭제 잘되었다는 창 띄우고,
    #   - 원래 페이지로 가기..
    url = "/pet/find/"

    msg = """
    <script type='text/javascript'>
        alert('삭제 되었습니다!');
        location.href = '{}';
    </script>
    """.format(url)  
    
    return HttpResponse(msg)

def FindUpdateView(request) :
    try:
        if request.method == "GET" :
            req_no = request.GET["req_no"]
            f_mem_id = request.GET["f_mem_id"]
            
        elif request.method == "POST" :
            req_no = request.POST["req_no"]
            f_mem_id = request.POST["f_mem_id"]          
            

        dog = find.FindUpdateView(req_no, f_mem_id)
        #return HttpResponse(dog)
    except:
        msg = """
                <script type='text/javascript'>
                        alert('수정중 에러가 발생하였습니다!');
                        history.go(-1);
                </script>
        """
        return HttpResponse(msg)
    
    return render(request,
        "petmgapp/find/find_update_view.html",
            {"dog" : dog})

def getSupportList(request):
    try :
        spt_eve,spt_one,eve_money, one_money = support.getSupportList(request.session["ses_mem_id"])
            
    except :
        url = "/pet/login_logout/"

        msg="""
            <script type='text/javascript'>
                alert('잘못된 접근입니다. 로그인하세요');
                location.href ='{}';
            </script>
        """.format(url) 

        return HttpResponse(msg)
    
    data = {"spt_eve":spt_eve,
            "spt_one":spt_one,
            "eve_money":eve_money[0],
            "one_money":one_money[0]}
    
    return render(request,
                "petmgapp/login/my_support.html",
                data)


def FindUpdate(request):
        try:
            if request.FILES['popfile'] :
                popfile = request.FILES['popfile']
        except:
            msg = """
                    <script type='text/javascript'>
                        alert('잘못된 접근입니다. 다시 입력하세요!');
                        location.href = '/pet/find/'
                    </script>
            """
            return HttpResponse(msg)
    
        ############################################
        #############[파일 업로드 처리]###############
        ### 파일 업로드 폴더 위치 지정
        upload_dir = "./petmgapp/static/petmgapp/file_manager/"
        
        ### 파일 다운로드 폴더 위치 지정
        down_dir = "/static/petmgapp/file_manager/"
        
        ### 파일 처리를 위한 클래스 생성 
        fu = File_Util()
        fu.setUpload(popfile, upload_dir, down_dir)
        fu.fileUpload()
        
        ### 파일사이즈
        file_size = fu.file_size
        
        ### 다운로드 파일명(경로 + 파일명) 
        file_full_name = fu.file_full_name
        
        ### 다운로드를 위해 DB의 파일명만 추출하기
        # /static/nonmodelapp/file_manager/dog01_aU2bFG7.jpg을 
        # "/" 기호로 split한 후 마지막 위치의 index번호 값 추출
        filename = file_full_name.split("/")[-1]
        
        ### 다운로드를 위한 파일명(전체경로 + 파일명)
        downFullName = "/static/petmgapp/file_manager/"+filename
            
        ### 테이블에 입력 시 아래처럼 파일명 처리
        # 사용하시는 테이블 내에 컬럼명이 downFullName 이라고 한다면...
        # "Insert into 테이블명 (컬럼명1, 컬럼명2, downFullName) 
        #     values({}, {}, '{}')".format(값1, 값2, downFullName) 
        ######################################### 

        try:
                ### 사용자가 입력한 값들 추출하기
                ### get 방식 처리
            if request.method == "GET" :
                    req_no = request.POST.get("req_no","") 
                    processstate = request.GET.get("processstate","") 
                    happendt = request.GET.get("happendt","")  
                    happenplace = request.GET.get("happenplace","") 
                    kindcd = request.GET.get("kindcd","") 
                    colorcd = request.GET.get("colorcd","") 
                    age = request.GET.get("age","")  
                    sexcd = request.GET.get("sexcd","") 
                    neuteryn = request.GET.get("neuteryn","") 
                    specialmark = request.GET.get("specialmark","") 

            ### post 방식 처리
            elif request.method == "POST" :
                    req_no = request.POST.get("req_no","") 
                    processstate = request.POST.get("processstate","") 
                    happendt = request.POST.get("happendt","")  
                    happenplace = request.POST.get("happenplace","") 
                    kindcd = request.POST.get("kindcd","") 
                    colorcd = request.POST.get("colorcd","") 
                    age = request.POST.get("age","")  
                    sexcd = request.POST.get("sexcd","") 
                    neuteryn = request.POST.get("neuteryn","") 
                    specialmark = request.POST.get("specialmark","") 
                    

            data = {
                    'req_no' : req_no,
                    'f_mem_id' : request.session["ses_mem_id"],
                    'popfile' : downFullName,
                    'processstate': processstate, 
                    'happendt': happendt,
                    'happenplace': happenplace,
                    'kindcd': kindcd,
                    'colorcd': colorcd,
                    'age': age,
                    'sexcd': sexcd,
                    'neuteryn': neuteryn,
                    'specialmark': specialmark
                    }    
            
            find.FindUpdate(data)
                
            #return HttpResponse(data["req_no"])
            #return HttpResponse(data["f_mem_id"])
                
                # return HttpResponse(data["happendt"])
                # return HttpResponse(data["happenplace"])
                # return HttpResponse(data["kindcd"])
                # return HttpResponse(data["colorcd"])
                # return HttpResponse(data["age"])
                # return HttpResponse(data["sexcd"])
                # return HttpResponse(data["neuteryn"])
                # return HttpResponse(data["specialmark"])
                                            
        except:
                msg = """
                        <script type='text/javascript'>
                                alert('수정중 에러가 발생하였습니다!');
                                history.go(-1);
                        </script>
                """
                return HttpResponse(msg)
            
        ### 저장 잘되었다는 창 띄우고,
        #   - 원래 페이지로 가기..
        url = "/pet/find/"
    
        msg = """
        <script type='text/javascript'>
            alert('수정 되었습니다!');
            location.href = '{}';
        </script>
        """.format(url)  
        
        return HttpResponse(msg)