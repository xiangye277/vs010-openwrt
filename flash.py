"""
VS010 固件刷入脚本
用法: python vs010_flash.py <固件文件.img>
"""
import requests
import base64
import re
import sys
import os

BASE = 'http://192.168.2.1'
PASSWORD = 'mzxgfwlpt00'

def login():
    """登录 VS010，返回 (session, stok)"""
    pwd_b64 = base64.b64encode(PASSWORD.encode()).decode()
    s = requests.Session()
    resp = s.post(f'{BASE}/api',
                  data=f'luci_username=user&luci_password={pwd_b64}',
                  allow_redirects=False,
                  timeout=10)
    if resp.status_code != 302:
        print(f"登录失败: HTTP {resp.status_code}")
        return None, None
    
    loc = resp.headers.get('Location', '')
    stok = re.search(r'stok=([a-f0-9]+)', loc)
    if not stok:
        print("无法提取 stok")
        return None, None
    
    stok_val = stok.group(1)
    print(f"登录成功 stok={stok_val}")
    return s, stok_val

def flash_firmware(session, stok, firmware_path):
    """上传固件到 VS010"""
    fsize = os.path.getsize(firmware_path)
    fname = os.path.basename(firmware_path)
    print(f"固件: {fname} ({fsize/1024/1024:.1f}MB)")
    
    if not fname.endswith('.img'):
        print("警告: 固件扩展名不是 .img，可能被拒绝")
    
    url = f'{BASE}/api/;stok={stok}/admin/advance/upgrade'
    
    with open(firmware_path, 'rb') as f:
        print(f"上传到 {url} ...")
        resp = session.post(url,
                          files={'file': (fname, f, 'application/octet-stream')},
                          data={'size': str(fsize)},
                          timeout=120)
    
    print(f"响应: HTTP {resp.status_code}")
    print(f"内容: {resp.text[:500]}")
    
    try:
        result = resp.json()
        if result.get('result', {}).get('result') == '0':
            print("✅ 固件上传成功!")
            if result.get('isreboot') == '1':
                print("🔄 路由器正在重启以应用新固件...")
                print("等待 2-3 分钟后路由器将以 OpenWrt 重启")
            else:
                print("⚠️ 固件已上传但未触发重启，检查响应")
        else:
            print(f"❌ 上传失败: {result.get('msg', '未知错误')}")
    except:
        print(f"原始响应: {resp.text}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python vs010_flash.py <固件文件.img>")
        sys.exit(1)
    
    firmware = sys.argv[1]
    if not os.path.exists(firmware):
        print(f"文件不存在: {firmware}")
        sys.exit(1)
    
    s, stok = login()
    if not s:
        sys.exit(1)
    
    flash_firmware(s, stok, firmware)
