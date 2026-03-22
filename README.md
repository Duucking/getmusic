# 通过命令行下载音乐
主要功能：调用GD Studio's官方API([点击跳转](https://music-api.gdstudio.xyz/api.php))，搜索平台音乐，并下载音乐文件到本地

音乐来源：netease, tencent, tidal, spotify, ytmusic, qobuz, joox, deezer, migu, kugou, kuwo, ximalaya, apple
使用示例：
```python
# 搜索下载名字为苏公堤的歌曲(默认搜索来源是酷我，默认下载路径为C盘用户下载目录)
python main.py 苏公堤
# 如果搜索到的歌曲不是想要的，可以加上歌手名模糊搜索，如果这样也搜不到，说明这个平台没有版权，指定其他平台试试
python main.py 杨一歌苏公堤
# 从网易云搜索下载名字为苏公堤的歌曲
python main.py 苏公堤 netease
# 从网易云搜索下载名字为苏公堤的歌曲，并保存在D盘的music文件夹
python main.py 苏公堤 netease "D:/music"
```
