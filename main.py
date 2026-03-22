import sys

from util.downloadmusic import download_music
from util.searchmusic import search_music


if __name__ == "__main__":
    # 如果命令行参数1为空则直接提示用户，退出程序
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print("😵请提供搜索关键词")
        sys.exit(1)
    # 如果命令行参数2为空则默认使用酷我平台
    if len(sys.argv) < 3 or not sys.argv[2].strip():
        source = "kuwo"
    else:
        source = sys.argv[2]
    # 如果命令行参数3为空则默认使用None路径
    if len(sys.argv) < 4 or not sys.argv[3].strip():
        download_path = None
    else:
        download_path = sys.argv[3]
    search_results = search_music(sys.argv[1], source=source)
    # 如果搜索结果为空则提示用户没有找到相关歌曲，退出程序
    if not search_results:
        print("🫤没有找到相关歌曲")
        sys.exit(1)
    # 下载第一首搜索结果的音乐
    download_music(search_results, path=download_path)