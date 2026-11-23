"""Optional offline-injected browser smoke test: python tests/browser_smoke.py"""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
RAW=(ROOT/'docs/index.html').read_text(encoding='utf-8')
STYLE=(ROOT/'docs/style.css').read_text(encoding='utf-8')
SCRIPT=(ROOT/'docs/app.js').read_text(encoding='utf-8')
HTML=RAW.replace('<link rel="stylesheet" href="./style.css">','<style>'+STYLE+'</style>')
HTML=HTML.replace('<script defer src="./app.js"></script>','')
HTML=HTML.replace('</body>','<script>'+SCRIPT+'</script></body>')
def main():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
        for label,width,height in [('desktop',1380,900),('mobile',390,844),('small',375,812)]:
            page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
            errors=[]
            page.on('pageerror',lambda err:errors.append(str(err)))
            page.set_content(HTML,wait_until='load')
            page.wait_for_timeout(220)
            page.evaluate("document.getElementById('toast').classList.remove('show')")
            title=page.title()
            overflow=page.evaluate('document.documentElement.scrollWidth>window.innerWidth')
            page.screenshot(path=str(ROOT/f'{label}.png'),full_page=False)
            print(label, 'title',title,'overflow',overflow,'errors',errors)
            assert not overflow, f'Horizontal overflow at {width}px'
            assert not errors, errors
            page.close()
        page=browser.new_page(viewport={'width':1365,'height':900})
        page.set_content(HTML)
        page.locator('input.day-checkbox').first.check()
        assert page.locator('#progressValue').inner_text()=='5%'
        page.locator('details.lesson-detail').first.locator('summary').click()
        assert page.locator('details.lesson-detail').first.get_attribute('open') is not None
        page.locator('#lessonSearch').fill('GitHub')
        assert 0<page.locator('article.lesson-card:visible').count()<12
        page.locator('#lessonSearch').fill('')
        page.locator('#promptSearch').fill('API')
        assert page.locator('article.prompt-item:visible').count()>=1
        page.locator('#promptSearch').fill('')
        page.locator('#genGoal').fill('做一个虚构简历测试页面')
        page.locator('#genOutcome').fill('手机375px无横向溢出')
        page.locator('#genRules').fill('不处理真实客户数据')
        page.locator('#generatePrompt').click()
        assert page.locator('#genResult').is_visible()
        assert '虚构简历' in page.locator('#genOutput').inner_text()
        page.locator('#exportProgress').click()
        assert '进度文件已导出' in page.locator('#toast').inner_text()
        print('interactions passed: progress/search/generator/export')
        browser.close()

if __name__=="__main__":
    main()
