"""轮询 VS010 OpenWrt GitHub Actions 编译状态"""
import urllib.request
import json
import time
import os

TOKEN = os.environ.get('GH_POLL_TOKEN', '')
RUN_ID = '28218536223'
REPO = 'xiangye277/vs010-openwrt'
OUTPUT_FILE = 'D:/HermesAgent/hermes-data/workspace/vs010-openwrt/build_result.txt'

for i in range(30):  # max 5 hours
    try:
        req = urllib.request.Request(
            f'https://api.github.com/repos/{REPO}/actions/runs/{RUN_ID}',
            headers={
                'Authorization': f'Bearer {TOKEN}',
                'Accept': 'application/vnd.github+json',
                'User-Agent': 'Hermes'
            }
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            status = data.get('status', '?')
            conclusion = data.get('conclusion', '?')
            ts = time.strftime('%H:%M:%S')
            msg = f'{ts} Status: {status} | Conclusion: {conclusion}'
            print(msg)
            
            if status == 'completed':
                print(f'\nBUILD FINISHED! Conclusion: {conclusion}')
                
                # Get artifacts
                req2 = urllib.request.Request(
                    f'https://api.github.com/repos/{REPO}/actions/runs/{RUN_ID}/artifacts',
                    headers={
                        'Authorization': f'Bearer {TOKEN}',
                        'Accept': 'application/vnd.github+json',
                        'User-Agent': 'Hermes'
                    }
                )
                with urllib.request.urlopen(req2, timeout=15) as resp2:
                    ad = json.loads(resp2.read())
                    for a in ad.get('artifacts', []):
                        print(f"Artifact: {a['name']} ({a['size_in_bytes']} bytes)")
                        print(f"Download: gh run download {RUN_ID} -R {REPO}")
                
                # Write result
                with open(OUTPUT_FILE, 'w') as f:
                    f.write(f'status={status}\nconclusion={conclusion}\n')
                break
    except Exception as e:
        print(f'Error: {e}')
    
    time.sleep(600)  # 10 minutes

print('Done polling')
