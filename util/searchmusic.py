import requests
import json

def search_music(name, source="netease", count=20, pages=1):
    """
    获取音乐搜索列表
    
    参数:
    name (str): 关键字，可以是曲目名、歌手名、专辑名（必填）
    source (str): 音乐源，可选项，默认为'netease'
                 可选值: netease(默认), tencent, tidal, spotify, ytmusic, qobuz, joox, deezer, migu, kugou, kuwo, ximalaya, apple
                 高级用法: 在音乐源后加上"_album"，如"netease_album"，可获取专辑中的曲目列表
    count (int): 页面长度，一次返回显示多少内容，默认为20条
    pages (int): 页码，返回搜索结果第几页，默认为第1页
    
    返回:
    list: 包含音乐信息的字典列表，每个字典包含以下字段:
          id: 曲目ID（track_id）
          name: 歌曲名
          artist: 歌手列表
          album: 专辑名
          pic_id: 专辑图ID
          url_id: URL ID（废弃）
          lyric_id: 歌词ID
          source: 音乐源
    """
    base_url = "https://music-api.gdstudio.xyz/api.php"
    
    # 构建请求参数
    params = {
        'types': 'search',
        'source': source,
        'name': name,
        'count': count,
        'pages': pages
    }
    
    print("🤔正在搜索音乐...")
    
    try:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        # 发送GET请求
        response = requests.get(base_url, params=params, headers=headers)
        
        # 检查响应状态
        if response.status_code == 200:
            # 解析JSON响应
            data = response.json()
            
            # 根据API返回结构，提取音乐列表
            # 假设返回的数据格式为包含music列表的字典
            if isinstance(data, list):
                print("🙂搜索完毕")
                return data
            elif isinstance(data, dict) and 'music' in data:
                print("🙂搜索完毕")
                return data['music']
            elif isinstance(data, dict):
                # 如果直接返回的是单个音乐对象或其它格式，则尝试返回整个数据
                print("🙂搜索完毕")
                return [data] if data else []
            else:
                return []
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON解析异常: {e}")
        return []

# 示例使用
if __name__ == "__main__":
    # 在酷我平台搜索名字为苏公堤的歌曲
    results = search_music(name="苏公堤", source="kuwo", count=10, pages=1)
    
    if results:
        print(f"找到 {len(results)} 首相关歌曲:")
        for i, music in enumerate(results[:5], 1):  # 只显示前5首
            print(f"{i}. {music.get('name', '未知歌曲')} - {music.get('artist', ['未知歌手'])[0]}")
            print(f"   专辑: {music.get('album', '未知专辑')}")
            print(f"   ID: {music.get('id', '无ID')}")
            print(f"   音乐源: {music.get('source', '未知源')}")
            print("-" * 40)
    else:
        print("未找到相关音乐")
