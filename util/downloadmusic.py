import os
import requests
from urllib.parse import urlparse
import time

def download_music(music_list, download_count=1, quality=999, path=None):
    """
    下载音乐
    
    参数:
    music_list (list): 音乐列表，每个元素为字典，包含id、source、name、artist(列表)
    download_count (int): 下载数量，默认为1，下载传入列表中第一首音乐
    quality (int): 音质，默认为740，可选128、192、320、740、999
    path (str): 保存路径，默认为C盘用户Download目录
    """
    # 设置默认下载路径
    if path is None:
        # 如果是Windows系统，使用用户下载目录；如果是其他系统，使用当前目录下的Music文件夹
        if os.name == 'nt':  # Windows
            path = os.path.join(os.path.expanduser("~"), "Downloads/Music")
        else:  # 其他系统
            path = os.path.join(os.getcwd(), "Music")
    
    # 确保下载路径存在
    os.makedirs(path, exist_ok=True)
    
    # 限制下载数量不超过列表长度
    download_count = min(download_count, len(music_list))
    
    downloaded_files = []
    
    for i in range(download_count):
        music_info = music_list[i]
        
        # 获取音乐信息
        music_id = music_info.get('id')
        source = music_info.get('source', 'netease')
        name = music_info.get('name', '未知歌曲')
        artist = music_info.get('artist', ['未知歌手'])
        
        if not music_id:
            print(f"音乐信息缺少ID，跳过: {name}")
            continue
        
        # 获取音乐下载链接
        print("🤔正在获取下载链接...")
        download_url = get_music_download_url(music_id, source, quality)
        
        if not download_url:
            print(f"无法获取音乐下载链接，跳过: {name}")
            continue
        
        print("🙂获取下载链接完毕")
        # 构造文件名
        if isinstance(artist, list):
            if len(artist) > 1:
                artist_str = ','.join(artist)
            else:
                artist_str = artist[0] if artist else '未知歌手'
        else:
            artist_str = str(artist)
        
        # 获取download_url中的文件后缀
        parsed_url = urlparse(download_url)
        file_extension = os.path.splitext(parsed_url.path)[1]

        # 清理文件名中的非法字符
        filename = f"{artist_str} - {name}{file_extension}"
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.', '(', ')', ','))
        
        # 确保文件名不过长
        if len(filename) > 200:
            filename = filename[:200] + file_extension
        
        file_path = os.path.join(path, filename)
        
        # 下载音乐
        print("🤔正在下载音乐...")
        success = download_file(download_url, file_path)
        
        if success:
            downloaded_files.append(file_path)
            print(f"🥰下载成功: {filename}")
        else:
            print(f"😫下载失败: {filename}")
        
        # 添加延迟避免请求过于频繁
        time.sleep(1)
    
    return downloaded_files

def get_music_download_url(music_id, source='netease', quality=740):
    """
    获取音乐下载链接
    
    参数:
    music_id (str): 音乐ID
    source (str): 音乐源
    quality (int): 音质
    
    返回:
    str: 音乐下载链接，如果获取失败则返回None
    """
    api_url = f"https://music-api.gdstudio.xyz/api.php"
    
    params = {
        'types': 'url',
        'source': source,
        'id': music_id,
        'br': quality
    }
    # 构造headers，模拟浏览器请求
    
    
    try:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(api_url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, dict) and 'url' in data:
                return data['url']
            else:
                print(f"API返回格式异常: {data}")
                return None
        else:
            print(f"获取音乐下载链接失败，状态码: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {e}")
        return None
    except Exception as e:
        print(f"获取音乐下载链接时发生错误: {e}")
        return None

def download_file(url, file_path):
    """
    下载文件到指定路径
    
    参数:
    url (str): 文件URL
    file_path (str): 保存路径
    
    返回:
    bool: 是否下载成功
    """
    try:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, stream=True, headers=headers)
        
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return True
        else:
            print(f"下载文件失败，状态码: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"下载文件时网络异常: {e}")
        return False
    except Exception as e:
        print(f"下载文件时发生错误: {e}")
        return False

# 示例使用
if __name__ == "__main__":
    # 示例音乐列表
    music_list = [
        {
            "id": "400981",
            "source": "netease",
            "name": "青花瓷",
            "artist": ["周杰伦"]
        },
        {
            "id": "185994",
            "source": "netease",
            "name": "稻香",
            "artist": ["周杰伦"]
        },
        {
            "id": "27833542",
            "source": "netease",
            "name": "夜曲",
            "artist": ["周杰伦"]
        }
    ]
    
    # 下载第一首音乐
    downloaded_files = download_music(
        music_list=music_list,
        download_count=1,
        quality=320,
        path=os.path.join(os.path.expanduser("~"), "Music")
    )
    
    print(f"下载完成，共下载 {len(downloaded_files)} 首音乐")
    for file in downloaded_files:
        print(f"- {file}")
