"""Validate the public deployment, with retries for Pages propagation."""
from pathlib import Path
from hashlib import sha256
from urllib.request import Request, urlopen
import time
ROOT=Path(__file__).resolve().parents[1]/'docs'
BASE='https://aipmandy.github.io/antigravity-guide/'
FILES=['index.html','app.js','style.css','robots.txt','sitemap.xml','pdf/antigravity-guide.pdf']

def main():
    expected={name:sha256((ROOT/name).read_bytes()).hexdigest() for name in FILES}
    for attempt in range(18):
        failures=[]
        for name in FILES:
            try:
                req=Request(BASE+name,headers={'User-Agent':'Antigravity-Pages-QA/1.0','Cache-Control':'no-cache'})
                with urlopen(req,timeout=15) as response:
                    body=response.read()
                    if response.status != 200 or sha256(body).hexdigest()!=expected[name]:
                        failures.append(f'{name}: HTTP {response.status} or SHA mismatch')
            except Exception as exc:failures.append(f'{name}: {exc}')
        if not failures:
            print('PASS: all six public Pages resources HTTP 200 and SHA-256 match')
            for name in FILES:print(f'{name}: {expected[name]}')
            return
        print(f'Attempt {attempt+1}: {failures}',flush=True)
        if attempt<17:time.sleep(8)
    raise SystemExit('FAIL: source and public Pages do not match')
if __name__=='__main__':main()
