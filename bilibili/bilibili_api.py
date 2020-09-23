import requests

g_hs = requests.Session()

platform = "web"
parent_area_id = 10
cate_id = 0
area_id = 33
sort_type = "online"
tag_vesion = 1

topRoomNum = 50

def getRoomList():
    totalRoomCount = 0
    page_index = 1
    page_size = 50

    url = 'https://api.live.bilibili.com/room/v3/area/getRoomList?platform={}&parent_area_id={}&cate_id={}&area_id={}&sort_type={}&tag_version={}'.format(platform, parent_area_id, cate_id, area_id, sort_type, tag_vesion)

    roomList = []
    roomCount = 0
    while True:
        nextUrl = (url+'&page={}&page_size={}').format(page_index, page_size)
        print(nextUrl)
        resp = g_hs.get(url=nextUrl).json()

        if not resp:
            raise Exception("获取影音馆直播列表失败！")
        elif resp["code"] != 0:
            raise Exception("获取影音馆直播列表失败！{}".format(resp["msg"]))
        
        data = resp["data"]
        totalRoomCount = data["count"]
        jsonRoomList = data["list"]
        roomCount = roomCount + len(data["list"])
        print("直播房间进度：{}/{}".format(roomCount,topRoomNum))

        for roomInfo in jsonRoomList:
            roomId = roomInfo["roomid"]
            roomName = roomInfo["title"]
            roomOwner = roomInfo["uname"]

            roomList.append((roomId, roomName, roomOwner))
        maxRoomNum = topRoomNum if topRoomNum <= totalRoomCount else totalRoomCount
        ifContinue = True if roomCount < maxRoomNum  else False
        if not ifContinue:
            break
        page_size = page_size if (maxRoomNum-roomCount) > page_size else maxRoomNum-roomCount
    return roomList

def getRealRoomId(roomId):
    url = 'https://api.live.bilibili.com/room/v1/Room/room_init?id={}'.format(roomId)
    resp = g_hs.get(url).json()
    if not resp:
        raise Exception("房间号错误！房间号：{}".format(roomId))

    code = resp['code']
    if code == 0:
        live_status = resp['data']['live_status']
        if live_status == 1:
            realRoomId = resp['data']['room_id']
            return realRoomId
        else:
            raise Exception("房间未开播！房间号：{}".format(roomId))
    else:
        raise Exception("获取房间开播信息失败！房间号：{}, {}".format(roomId, resp["message"]))


def getPlayUrl(realRoomId, platForm="web"):
    url = 'https://api.live.bilibili.com/xlive/web-room/v1/playUrl/playUrl'
    params = {
        'cid': realRoomId,
        'qn': 10000,
        'platform': platForm,
        'https_url_req': 1,
        'ptype': 16
    }
    resp = g_hs.get(url, params=params).json()
    if not resp:
        raise Exception("房间号不存在：{}".format(realRoomId))
    try:
        durl = resp['data']['durl']
        real_url = durl[-1]['url']
        return real_url
    except KeyError or IndexError:
        raise Exception('获取{}直播流链接失败！房间号：{}'.format(platForm, realRoomId))

