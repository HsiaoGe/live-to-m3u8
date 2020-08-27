# live-to-m3u8
经常把直播当工作背景音来用，但是需要开一个浏览器才行，而且浏览器有时候体验不好打开非常慢。所以想弄一个获取到直播流的脚本来生成m3u8播放列表，直接在播放器中播放,有些播放器还支持只听声音不需要画面，有些直播APP也支持。

## biliblli
直接执行`python3 main.py`，就可以在目录下生成一个`bilibili_live.m3u8`的媒体文件，可以直接用播放器打开，在列表栏就可以看到直播列表。
获取的是`放映厅`的综合排名前50的直播房间，里面有很多相声直播间，这下可以安心听相声工作了。
获取到的`bilibili`直播流链接一般都是一个小时的有效时间，但并不是到了一个小时，正在播放的直播会停止，重新播放的时候才会失效。
注意不要频繁请求房间信息，会被`bilibili`拦截，当发现直播链接失效的时候再运行脚本重新生成。
`bilibili`的`API`是从下面两个仓库获取的，房间列表是从网页上爬的。
- [real-url](https://github.com/wbt5/real-url) 
- [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) 


