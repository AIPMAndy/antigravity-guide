#!/usr/bin/env python3
"""Render a mobile-friendly A5 PDF from the same editorial source."""
from pathlib import Path
from html import escape
from weasyprint import HTML
from content_source import LESSONS,PROMPTS,PLAN,FAQ,SOURCES,UPDATED

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/pdf/antigravity-guide.pdf'
css='''
@page{size:A5;margin:14mm 13mm 16mm;@bottom-center{content:"AI 酋长 Andy · Google Antigravity 保姆级教程 · " counter(page);font-family:"Noto Sans CJK SC",sans-serif;font-size:7px;color:#8d9bb1}}
@page :first{@bottom-center{content:"AI 酋长 Andy · 2026";font-size:8px;color:#92a1b6}}
*{box-sizing:border-box}html{font-family:"Noto Sans CJK SC","Noto Sans SC",sans-serif;color:#24324c}body{font-size:9.5pt;line-height:1.79}h1,h2,h3,h4{line-height:1.38;break-after:avoid}h1{font-size:25pt;letter-spacing:-.5px;margin:0 0 16px}h2{font-size:15pt;letter-spacing:-.2px;margin:0 0 10px}h3{font-size:11pt;margin:17px 0 7px}p{margin:5px 0 10px}a{color:#305dd4;text-decoration:none}.cover{page-break-after:always;padding-top:12mm}.brand{font-size:8pt;letter-spacing:3px;font-weight:900;color:#4b70ce}.cover-line{width:38mm;height:3px;background:#3d6bea;margin:10mm 0 12mm}.cover h1{font-size:32pt;line-height:1.35;letter-spacing:-1.1px}.cover h1 em{font-style:normal;color:#396ae7}.cover-sub{font-size:12pt;color:#6b7a94;max-width:95mm;line-height:1.9}.cover-stats{display:flex;gap:4mm;margin-top:12mm;border-top:1px solid #dde6f5;padding-top:9mm}.cover-stats div{flex:1}.cover-stats b{display:block;font-size:20pt;line-height:1;color:#2e52a3}.cover-stats span{font-size:8pt;color:#8191a9}.meta{font-size:8pt;color:#8090aa;margin-top:8mm}.note{padding:10px 12px;border-left:3px solid #456de3;background:#f0f4fe;color:#506583;font-size:9pt;margin:15px 0;line-height:1.7}.chapter{page-break-before:always}.chapter-head{border-bottom:1px solid #dce4f2;padding-bottom:12px;margin-bottom:12px}.chapternum{font-size:8pt;color:#4068c7;font-weight:800;letter-spacing:1.5px}.chapter h2{font-size:20pt;margin:6px 0}.chapter-meta{font-size:8.5pt;color:#74849a}.step{break-inside:avoid;margin:12px 0}.step strong{display:block;font-size:10pt}.step p{margin:4px 0;font-size:9pt;color:#475970}.prompt{padding:13px 12px;background:#f0f4fc;border:1px solid #e0e8f4;border-radius:6px;margin:12px 0;white-space:pre-wrap;overflow-wrap:anywhere;font-size:8.5pt;line-height:1.7;color:#3d4e6c;break-inside:avoid}.checklist li,.pitfalls li{font-size:9pt;margin:3px 0}.checklist li::marker{color:#4970da}.sources{font-size:8pt;overflow-wrap:anywhere}.sources li{margin:4px 0}.toc{page-break-after:always}.toc li{padding:5px 0;border-bottom:1px solid #e9eef5;font-size:9pt}.toc strong{color:#4269ca}.section{page-break-before:always}.footer-note{font-size:8pt;color:#6c7f99;padding-top:12px;border-top:1px solid #e1e8f3}.promo{padding:15px;background:#1e3152;color:#fff;border-radius:8px;margin-top:15px}.promo h3{color:#fff}.promo p{color:#c2d0e7;font-size:8.5pt}.promo a{color:#9ec1ff}
'''

def esc(t):return escape(t,quote=True)
parts=['<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>'+css+'</style></head><body>']
parts.append(f'''<section class="cover"><div class="brand">A N T I G R A V I T Y &nbsp; / &nbsp; F I E L D &nbsp; G U I D E</div><div class="cover-line"></div><h1>Google Antigravity<br><em>保姆级实战教程</em></h1><p class="cover-sub">从第一次启动，到一个真正可以运行、测试和发布的 AI 产品。</p><p class="note">不是空谈 Agent：每章都有操作步骤、任务指令、验收标准与风险边界。内容独立制作，非 Google 官方。</p><div class="cover-stats"><div><b>12</b><span>章节</span></div><div><b>18</b><span>Prompt</span></div><div><b>07</b><span>天计划</span></div><div><b>02</b><span>项目路径</span></div></div><p class="meta">AI 酋长 Andy · 版本 1.0 · 内容核查 {UPDATED}<br>metaver.vip · 微信 AIPMAndy<br>免费阅读 · 开源许可 MIT</p></section>''')
parts.append('<section class="toc"><div class="brand">CONTENTS</div><h1>从这里开始</h1><p>建议按顺序完成 01–03 章，再动手做 05、06 两个项目。前面完成不了的内容不必硬跳。</p><ol>')
for l in LESSONS:parts.append(f'<li><strong>{esc(l["id"])}</strong> &nbsp; {esc(l["title"])} <span style="color:#8999b0"> · {esc(l["time"])}</span></li>')
parts.append('</ol><p class="note">完整交互网站预计部署于 https://aipmandy.github.io/antigravity-guide/ 。以 GitHub Pages 实际部署状态为准。</p><p style="font-size:8pt;color:#697d95">官方入口：https://antigravity.google/download</p></section>')
parts.append('<section class="section"><div class="brand">THE SEVEN-DAY PLAN</div><h1>7 天上手计划</h1>')
for d,t,body in PLAN:parts.append(f'<div class="step"><strong>Day {esc(d)} · {esc(t)}</strong><p>{esc(body)}</p></div>')
parts.append('<p class="note">验收建议：每一天保存文件、截图、实际测试结果。不要只记录“今天学了什么”。</p></section>')
for l in LESSONS:
    parts.append(f'<section class="chapter"><div class="chapter-head"><div class="chapternum">CHAPTER {esc(l["id"])} / 12 · {esc(l["tag"])}</div><h2>{esc(l["title"])}</h2><div class="chapter-meta">时间：{esc(l["time"])} &nbsp; | &nbsp; 交付：{esc(l["deliverable"])}</div></div><p>{esc(l["context"])}</p><h3>一步步操作</h3>')
    for i,(t,body) in enumerate(l['steps'],1):parts.append(f'<div class="step"><strong>{i:02d} / {esc(t)}</strong><p>{esc(body)}</p></div>')
    parts.append(f'<h3>直接复制的 Agent 指令</h3><div class="prompt">{esc(l["prompt"])}</div>')
    parts.append('<h3>验收标准</h3><ul class="checklist">'+''.join(f'<li>{esc(x)}</li>' for x in l['accept'])+'</ul>')
    parts.append('<h3>避坑提醒</h3><ul class="pitfalls">'+''.join(f'<li>{esc(x)}</li>' for x in l['pitfalls'])+'</ul>')
    parts.append(f'<p class="sources">官方延伸：<a href="{esc(l["official"])}">{esc(l["official"])}</a></p></section>')
parts.append('<section class="section"><div class="brand">PROMPT TOOLKIT</div><h1>18 条可复制指令</h1><p>把下方的占位符 ____ 换成你的真实目标。不要输入账号、密码、客户隐私或密钥。</p>')
for i,(t,tag,body) in enumerate(PROMPTS,1):parts.append(f'<div class="step"><strong>{i:02d} / {esc(t)} <small style="color:#7e8fa9">({esc(tag)})</small></strong><div class="prompt">{esc(body)}</div></div>')
parts.append('</section>')
parts.append('<section class="section"><div class="brand">FACTS & BOUNDARIES</div><h1>官方来源与注意事项</h1><p>当前版本内容核查：2026-11-23。界面、额度、套餐和地区可能改变，以官方当天的真实页面和账户状态为准。</p><ul class="sources">')
for t,url,desc in SOURCES:parts.append(f'<li><strong>{esc(t)}</strong>：{esc(desc)}<br><a href="{esc(url)}">{esc(url)}</a></li>')
parts.append('</ul><h3>安全底线</h3><ol><li>Agent 只进入授权目录，首先使用保守的审批配置。</li><li>不允许自动发布、删除、发送、收费或接触密钥。</li><li>只要没有实际执行测试，就不宣称通过。</li><li>项目演示数据全部虚构，真实业务须有客户授权。</li></ol></section>')
parts.append('<section class="section" style="padding-top:26mm"><div class="brand">NEXT STEPS</div><h1>下一步，做出一个<br>真正可以交付的作品。</h1><p style="font-size:12pt;line-height:1.8;color:#667a98;margin:10mm 0 20mm">你不需要先懂所有技术。<br>从一份清楚的需求开始，保留审批权、保留测试证据、保留恢复能力。<br>做完第一个，再做第二个。</p><div class="promo"><h3>关于 AI 酋长 Andy</h3><p>本手册和网站永久免费开放。AI 产品咨询、个人 IP 与企业 AI 增长陪跑是自愿选择的独立商业服务，与 Google 无官方合作关系。</p><p>官网：<a href="https://metaver.vip/">https://metaver.vip/</a><br>服务：<a href="https://metaver.vip/services">https://metaver.vip/services</a><br>微信：AIPMAndy</p></div></section>')
parts.append('</body></html>')
html=''.join(parts)
OUT.parent.mkdir(parents=True,exist_ok=True)
HTML(string=html,base_url=str(ROOT)).write_pdf(str(OUT))
print('Created',OUT,'bytes',OUT.stat().st_size)
