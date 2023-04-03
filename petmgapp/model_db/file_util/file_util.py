### 파일 업로드(저장) 처리를 위한 라이브러리
from django.core.files.storage import FileSystemStorage

### 파일 다운로드 처리를 위한 라이브러리
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import os
from django.http import HttpResponse



class File_Util :
    # - 파일 원본 정보
    file_nm = ""
    
    # - 파일 업로드 폴더 위치 지정
    upload_dir = ""
    
    # - 파일 다운로드 폴더 위치 지정
    down_dir = ""
    
    # - 파일 사이즈
    file_size = 0
    
    # - 이미지 등 페이지 static 경로 + 파일명
    file_full_name = ""
    
    # - 순수 파일명
    filename = ""
    
    # - 다운로드를 위한 전체경로 + 파일명
    downFullName = ""
    
    ### 업로드를 위해 멤버 변수 설정
    def setUpload(self, file_nm, upload_dir, down_dir) :
        self.file_nm    = file_nm
        self.upload_dir = upload_dir
        self.down_dir   = down_dir
    
    ### 파일 업로드 함수
    def fileUpload(self) :
        ### 파일 처리를 위한 클래스 생성
        fs = FileSystemStorage(self.upload_dir, self.down_dir)
        
        ### 파일을 save_dir 폴더에 저장하기
        # - save(파일명, 파일정보)
        self.filename = fs.save(self.file_nm.name, self.file_nm)
        
        # - 파일사이즈
        self.file_size = self.file_nm.size
        
        # - static 경로 + 파일명(경로 + 파일명) 
        self.file_full_name = fs.base_url + self.filename
        
    ### 다운로드를 위해 멤버 변수 설정
    def setDownload(self, downFullName) :
        self.downFullName = downFullName
        
    ### 파일 다운로드 함수
    def fileDownload(self) :
        binary_file = open(self.downFullName, 'rb')
        response = HttpResponse(binary_file.read(), 
                                content_type="application/octet-stream; charset=utf-8")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(self.downFullName)
        return response