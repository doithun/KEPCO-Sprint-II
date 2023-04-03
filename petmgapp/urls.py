from django.urls import path

from . import views

urlpatterns = [
    # http:127.0.0.1:8000//mem_list

    path('report_view/',views.getReport),  
    path('report_insert/',views.ReportInsert),  
    
    path('mem_insert_view/',views.getMemberInsert),
    path('mem_insert/',views.MemberInsert),
    
    path('mem_delete_view/',views.getDelete),
    path('mem_delete/',views.MemberDelete),

    path('login_logout/',views.login_logout),
    path('login/',views.login),
    path('logout/',views.logout),
    
    path('mem_my_view/',views.getMember),
    path('mem_update/',views.MemberUpdate),
    
    path('notice/',views.getNotice),
    path('protect/',views.getProtect),
    path('find/',views.getFind),
    
    path('notice_view/',views.getNoticeView),
    path('protect_view/',views.getProtectView),
    path('find_view/',views.getFindView),

    path('notice_search/',views.getNoticeSearch),
    path('protect_search/',views.getProtectSearch),
    path('find_search/',views.getFindSearch),
    
    path('find_delete/',views.FindDelete),
    path('find_update_view/',views.FindUpdateView),
    path('find_update/',views.FindUpdate),  
        
    path('support/',views.support),
    path('support_chk/',views.support_chk),
    path('support_view/',views.support_view),
    
    path('my_support_list/',views.my_support_list),
    
    path('dog_tip1/',views.getDogTip1),
    path('dog_tip2/',views.getDogTip2),   
    path('dog_tip3/',views.getDogTip3), 
    
    
    

]

