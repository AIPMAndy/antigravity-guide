"""Run against the real locally served GitHub Pages files, not injected HTML."""
from pathlib import Path
import contextlib, functools, json, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'browser-qa'
OUT.mkdir(exist_ok=True)
@contextlib.contextmanager
def server():
    handler=functools.partial(SimpleHTTPRequestHandler,directory=str(ROOT/'docs'))
    httpd=ThreadingHTTPServer(('127.0.0.1',0),handler)
    thread=threading.Thread(target=httpd.serve_forever,daemon=True);thread.start()
    try: yield f'http://127.0.0.1:{httpd.server_port}/'
    finally: httpd.shutdown();httpd.server_close();thread.join()

def main():
    with server() as url, sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        for width,scheme,reduce in [(360,'light','reduce'),(390,'dark','no-preference'),(1280,'light','no-preference')]:
            ctx=browser.new_context(viewport={'width':width,'height':844},color_scheme=scheme,reduced_motion=reduce,accept_downloads=True)
            page=ctx.new_page();errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
            page.goto(url,wait_until='load')
            assert page.locator('article.lesson-card:visible').count()==12
            assert page.locator('article.prompt-item:visible').count()==18
            assert page.locator('#resetProgress').is_disabled()
            page.screenshot(path=str(OUT/f'{width}-home.png'))
            if width<781:
                page.locator('#menuToggle').click();expect(page.locator('#mobileNav')).to_be_visible()
                page.keyboard.press('Escape');expect(page.locator('#mobileNav')).to_be_hidden()
                expect(page.locator('#menuToggle')).to_be_focused()
            first=page.locator('input.day-checkbox').first
            first.check();expect(page.locator('#progressRing')).to_have_attribute('aria-valuenow','5')
            page.reload();expect(first).to_be_checked()
            page.once('dialog',lambda d:d.dismiss());page.locator('#resetProgress').click();expect(first).to_be_checked()
            page.once('dialog',lambda d:d.accept());page.locator('#resetProgress').click();expect(first).not_to_be_checked()
            page.locator('#undoProgress').click();expect(first).to_be_checked()
            invalid=json.dumps({'version':1,'checked':{'day-2':True}}).encode()
            page.locator('#progressFile').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':invalid})
            expect(page.locator('#toast')).to_contain_text('没有可识别的课程进度')
            expect(first).to_be_checked()
            data=json.dumps({'version':1,'checked':{'day-02':True}}).encode()
            page.once('dialog',lambda d:d.dismiss())
            page.locator('#progressFile').set_input_files({'name':'backup.json','mimeType':'application/json','buffer':data})
            expect(page.locator('#toast')).to_contain_text('未替换')
            expect(first).to_be_checked()
            page.once('dialog',lambda d:d.accept())
            page.locator('#progressFile').set_input_files({'name':'backup.json','mimeType':'application/json','buffer':data})
            expect(page.locator('input[data-key="day-02"]')).to_be_checked()
            expect(first).not_to_be_checked()
            page.locator('#undoProgress').click();expect(first).to_be_checked()
            with page.expect_download() as d: page.locator('#exportProgress').click()
            saved=json.loads(Path(d.value.path()).read_text());assert saved['checked']['day-01'] is True
            page.locator('#lessonSearch').fill('GitHub')
            n=page.locator('article.lesson-card:visible').count();assert 0<n<12
            expect(page.locator('#lessonCount')).to_have_text(f'{n} / 12 项')
            page.locator('#lessonReset').click();expect(page.locator('#lessonSearch')).to_be_focused()
            expect(page.locator('#lessonCount')).to_have_text('12 / 12 项')
            page.locator('details.lesson-detail').first.locator('summary').click()
            assert page.locator('details.lesson-detail').first.get_attribute('open') is not None
            page.locator('#promptSearch').fill('___no_matching_source___')
            expect(page.locator('#promptEmpty')).to_be_visible()
            page.locator('#promptReset').click()
            expect(page.locator('#promptCount')).to_have_text('18 / 18 项')
            page.locator('#genGoal').fill('做一个虚构简历测试页面')
            page.locator('#genOutcome').fill('手机375px无横向溢出')
            page.locator('#genRules').fill('不处理真实客户数据')
            page.locator('#generatePrompt').click();expect(page.locator('#genResult')).to_be_visible()
            expect(page.locator('#genOutput')).to_contain_text('虚构简历')
            page.locator('#genRules').fill('不连接生产账户')
            expect(page.locator('#genResult')).to_be_hidden()
            expect(page.locator('#copyGenerated')).to_be_disabled()
            expect(page.locator('#genStatus')).to_contain_text('重新生成')
            page.locator('#generatePrompt').click()
            expect(page.locator('#genOutput')).to_contain_text('不连接生产账户')
            if reduce=='reduce':
                assert page.locator('.btn').first.evaluate('(el)=>getComputedStyle(el).transitionDuration')=='0s'
            assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth+2'), width
            assert not errors,errors
            page.screenshot(path=str(OUT/f'{width}-prompt.png'))
            print(f'PASS {width}px, system {scheme}, motion={reduce}: progress/undo/import/export/search/prompt/menu')
            ctx.close()
        browser.close()
if __name__=='__main__': main()
