import requests
import pandas as pd
import numpy as np
import folium
from folium.plugins import MiniMap
import collections
from IPython.display import HTML, display

REST_API_KEY = '40bf37ec6689f376c24117c4141177aa'
JAVASCRIPT_API_KEY = '8b14283f3bf537ccd22fe68d71c20366'
    
def place_location(region, page_num):
    
    # 주소로 검색하기
    url = 'https://dapi.kakao.com/v2/local/search/address.json'
    params = {'query': region,'page': page_num}
    headers = {"Authorization": f"KakaoAK {REST_API_KEY}"}

    places = requests.get(url, params=params, headers=headers).json()['documents']
    # print(len(places))
    total = requests.get(url, params=params, headers=headers).json()['meta']['total_count']
    # print(total)   
        
    if total > 45:
        print(total,'개 중 45개 데이터밖에 가져오지 못했습니다!')
    else :
        print('모든 데이터를 가져왔습니다!')
        
    return places

def place_info(places):
    X = [] #경도
    Y = [] #위도
    building_name = [] #빌딩 이름
    address_name = [] #전체 지번 주소
    zone_no = [] #우편번호
    for i in range(len(places)):
        X.append(float(places[i]['x']))
        Y.append(float(places[i]['y']))
        building_name.append(places[i]['road_address']['building_name'])
        address_name.append(places[i]['address']['address_name'])
        zone_no.append(places[i]['road_address']['zone_no'])

    ar = np.array([zone_no, building_name, X, Y, address_name]).T
    df = pd.DataFrame(ar, columns = ['zone_no','building_name', 'X', 'Y','address_name'])

    # print(ar)
    # print(df)
    return df

def address(location):
    df = None
    for loca in location:
        for page in range(1,4):
            local_name = place_location(loca, page)
            local_place_info = place_info(local_name)

            if df is None:
                df = local_place_info
            elif local_place_info is None:
                continue
            else:
                df = pd.concat([df, local_place_info],join='outer', ignore_index = True)
    return df

##지도로 보여주기
def make_map(dfs, criteria_x, criteria_y):
    # 지도 생성하기
    m = folium.Map(location=[criteria_y, criteria_x],   # 기준좌표: 제주어딘가로 내가 대충 설정
                    zoom_start=17)

    # 미니맵 추가하기
    minimap = MiniMap() 
    m.add_child(minimap)

    # 마커 추가하기
    for i in range(len(dfs)):
        folium.Marker([dfs['Y'][i],dfs['X'][i]],
                        tooltip=dfs['building_name'][i],
                        popup=dfs['address_name'][i],
                            ).add_to(m)
        
    return display(m)

def getLocation_info(location):
    df = address(location)
    
    df = df.drop_duplicates(['zone_no'])

    df = df.reset_index()
    
    if not df.empty :
        x = place_location(location, 1)[0]['address']['x']

        y = place_location(location, 1)[0]['address']['y']
        
        return df, x, y
    else :
        return False


def getKakaoMapHtml(carenm, y, x):
    javascript_key = JAVASCRIPT_API_KEY

    result = ""
    result = result + "<div id='map' style='width:800px;height:700px;display:inline-block;'></div>" + "\n"
    result = result + "<script type='text/javascript' src='//dapi.kakao.com/v2/maps/sdk.js?appkey=" + javascript_key + "'></script>" + "\n"
    result = result + "<script>" + "\n"
    result = result + "    var container = document.getElementById('map'); " + "\n"
    result = result + "    var options = {" + "\n"
    result = result + "           center: new kakao.maps.LatLng(" + y + ", " + x + ")," + "\n"
    result = result + "           level: 1" + "\n"
    result = result + "    }; " + "\n"
    
    # 지도 생성
    result = result + "    var map = new kakao.maps.Map(container, options); " + "\n"

    # 마커이미지의 주소입니다   
    result = result + " var imageSrc = '../../static/petmgapp/img/dog_paw.svg', " + "\n"
    
    # 마커이미지의 크기입니다
    result = result + " imageSize = new kakao.maps.Size(35, 40), " + "\n"
    
    # 마커이미지의 옵션입니다. 마커의 좌표와 일치시킬 이미지 안에서의 좌표를 설정합니다.
    result = result + " imageOption = {offset: new kakao.maps.Point(10, 50)}; " + "\n"

    # 마커의 이미지정보를 가지고 있는 마커이미지를 생성합니다
    result = result + " var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imageOption), " + "\n"
    
    # 마커가 표시될 위치입니다
    result = result + "  markerPosition = new kakao.maps.LatLng(" + y + ", " + x + "); " + "\n"
    
    # 일반 지도와 스카이뷰로 지도 타입을 전환할 수 있는 지도타입 컨트롤을 생성합니다
    result = result + " var mapTypeControl = new kakao.maps.MapTypeControl();" + "\n"

    # 지도에 컨트롤을 추가해야 지도위에 표시됩니다
    # kakao.maps.ControlPosition은 컨트롤이 표시될 위치를 정의하는데 TOPRIGHT는 오른쪽 위를 의미합니다
    result = result + " map.addControl(mapTypeControl, kakao.maps.ControlPosition.TOPRIGHT);" + "\n"
    
    # 줌 기능 
    result = result + "    var zoomControl = new kakao.maps.ZoomControl(); " + "\n"
    result = result + "    map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT); " + "\n"

    # 검색한 좌표의 마커 생성을 위해 추가
    result = result + "    var markerPosition  = new kakao.maps.LatLng(" + y + ", " + x + ");  " + "\n"
    
    # 마커 생성, 마커이미지 설정
    result = result + " var marker = new kakao.maps.Marker({position: markerPosition, image: markerImage}); " + "\n"

    # 마커가 지도 위에 표시되도록 설정합니다
    result = result + "    marker.setMap(map); " + "\n"
    
    # 인포윈도우에 표출될 내용으로 HTML 문자열이나 document element가 가능합니다
    result = result + """ var iwContent = "<div style='font-weight:bold; text-align:center; width: 230px; height: 60px; padding:5px 0;'>""" + carenm + """ <br><a href='https://map.kakao.com/link/map/""" + carenm + ""","""+ y +""","""+ x +""" ' style='text-align:center; color:blue;' target='_blank'>큰지도보기</a> <a href='https://map.kakao.com/link/to/""" + carenm + ""","""+ y +""","""+ x +""" ' style='text-align:center; color:blue;' target='_blank'>길찾기</a></div>", """+ "\n"
    
    # 인포윈도우 표시 위치입니다
    result = result + " iwPosition = new kakao.maps.LatLng(" + y + ", " + x + ");" + "\n"

    #  인포윈도우를 생성합니다
    result = result + " var infowindow = new kakao.maps.InfoWindow({   " + "\n"
    result = result + "     position : iwPosition,  " + "\n"
    result = result + "     content : iwContent " + "\n"
    result = result + "  }); " + "\n"
    
    # 마커 위에 인포윈도우를 표시합니다. 두번째 파라미터인 marker를 넣어주지 않으면 지도 위에 표시됩니다
    result = result + " infowindow.open(map, marker); " + "\n"
    
    result = result + "</script>" + "\n"
    
    return result
