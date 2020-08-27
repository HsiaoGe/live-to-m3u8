
from bilibili_api import getRealRoomId, getPlayUrl,getRoomList
import requests
import json

def main():
    roomList = getRoomList()
    if len(roomList) == 0:
        return

    roomInfoList = []
    for roomInfo in roomList:
        roomId = roomInfo[0]
        roomName = roomInfo[1]
        roomOwner = roomInfo[2]
        print("处理中，房间号：{}, 房间名：{}".format(roomId, roomName))
        try:
            realRoomId = getRealRoomId(roomId)
            playUrl = getPlayUrl(realRoomId)

            roomPlayInfo = {"roomId":realRoomId, "roomName":roomName, "roomOwner":roomOwner, "playUrl": playUrl}

            roomInfoList.append(roomPlayInfo)
        except Exception as e:
            print("异常：",e)
            continue
    write2M3U8(roomInfoList)
    

def write2Json(roomInfoList):
    if len(roomInfoList) > 0:
        roomInfoJsonStr = json.dumps(roomInfoList)
        dumpFile = open("./bilibili_room.json", "w")
        if dumpFile:
            dumpFile.write(roomInfoJsonStr)
            dumpFile.close()
        else:
            raise Exception("文件打开失败！")

def write2M3U8(roomInfoList):
    if len(roomInfoList) > 0:
        dumpFile = open("./bilibili_room.m3u8", "w")
        if dumpFile:
            for roomInfo in roomInfoList:
                roomName = roomInfo["roomName"]
                roomOwner = roomInfo["roomOwner"]
                playUrl = roomInfo["playUrl"]

                fileLine = "#EXTINF:0, {} - {}\n{}\n".format(roomName, roomOwner, playUrl)
                dumpFile.write(fileLine)
            dumpFile.close()
        else:
            raise Exception("文件打开失败！")

if __name__ == "__main__":
    main()