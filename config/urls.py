"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

### include 라이브러리 불러들이기
from django.urls import path, include

from petmgapp import views as pm

urlpatterns = [
    ### 페이지마다 하나씩 추가하기
    # http:127.0.0.1:8000/test/url로 요청이 들어오면,
    # - views.py 파일의 test 함수를 호출합니다. 
    # - url과 함수를 매핑한다고 합니다. => url패턴이라는 용어로 사용
    
    ### index 시작페이지
    path('index.html', pm.getBase),
    path('index', pm.getBase),  
    path('intro', pm.getIntro),
    path('', pm.getIntro),

    path('pet/', include('petmgapp.urls')), 
                
    path('admin/', admin.site.urls),
]