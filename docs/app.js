'use strict';
(() => {
  const STORAGE = 'andy-antigravity-guide-progress-v1';
  const items = [...document.querySelectorAll('input[data-key]')];
  const dayCount = document.querySelectorAll('.day-checkbox').length;
  const lessonCount = document.querySelectorAll('.lesson-checkbox').length;
  const toast = document.getElementById('toast');
  let noticeTimer = null;
  const notify = (message) => { toast.textContent = message; toast.classList.add('show'); clearTimeout(noticeTimer); noticeTimer = setTimeout(()=>toast.classList.remove('show'), 2800); };
  const currentState = () => Object.fromEntries(items.map(x => [x.dataset.key, x.checked]));
  const applyState = state => { items.forEach(x => {x.checked = state[x.dataset.key] === true;}); drawProgress(); };
  const drawProgress = () => {
    const done = items.filter(x=>x.checked).length;
    const percent = Math.round(100 * done / items.length);
    document.getElementById('progressRing').style.background = `conic-gradient(#3c6cf3 ${percent*3.6}deg,#e8eefb 0deg)`;
    document.getElementById('progressValue').textContent = percent + '%';
    document.getElementById('progressSubtitle').textContent = `${done} / ${items.length} 项已完成（${dayCount} 天 + ${lessonCount} 章）`;
  };
  try {const saved=JSON.parse(localStorage.getItem(STORAGE) || '{}'); if(saved && typeof saved==='object' && !Array.isArray(saved)) applyState(saved);} catch {notify('浏览器本地进度不可读取；仍可手动打卡并导出');}
  items.forEach(box=>box.addEventListener('change',()=>{drawProgress();try{localStorage.setItem(STORAGE,JSON.stringify(currentState()));}catch{notify('当前浏览器无法保存，建议手动导出进度');}}));
  drawProgress();
  const downloadText = (name,body,type) => {const blob=new Blob([body],{type});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1500);};
  document.getElementById('exportProgress').addEventListener('click',()=>{downloadText('antigravity-progress.json',JSON.stringify({version:1,exportedAt:new Date().toISOString(),checked:currentState()},null,2),'application/json;charset=utf-8');notify('进度文件已导出');});
  document.getElementById('importProgress').addEventListener('click',()=>document.getElementById('progressFile').click());
  document.getElementById('progressFile').addEventListener('change',async e=>{const file=e.target.files?.[0];if(!file)return;try{if(file.size>100000)throw Error('文件过大');const parsed=JSON.parse(await file.text());if(parsed?.version!==1||typeof parsed.checked!=='object'||!parsed.checked||Array.isArray(parsed.checked))throw Error('格式不匹配');const keys=new Set(items.map(x=>x.dataset.key));const safe={};for(const [k,v] of Object.entries(parsed.checked)){if(keys.has(k)){if(typeof v!=='boolean')throw Error('非布尔型进度');safe[k]=v;}}applyState(safe);try{localStorage.setItem(STORAGE,JSON.stringify(currentState()));}catch{}notify('进度已导入');}catch(err){notify('导入失败：'+err.message);}finally{e.target.value='';}});
  document.getElementById('resetProgress').addEventListener('click',()=>{if(!confirm('确定清空所有学习进度吗？此操作不会修改或删除项目文件。'))return;applyState({});try{localStorage.removeItem(STORAGE);}catch{}notify('本机打卡已清空');});
  async function copyText(text){try{if(navigator.clipboard?.writeText && window.isSecureContext){await navigator.clipboard.writeText(text);}else{const field=document.createElement('textarea');field.value=text;field.setAttribute('readonly','');field.style.position='fixed';field.style.left='-9999px';document.body.append(field);field.select();const ok=document.execCommand('copy');field.remove();if(!ok)throw Error('请手动复制');}notify('已复制到剪贴板');}catch{notify('复制失败，请选择文本手动复制');}}
  document.querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',()=>copyText(button.dataset.copy)));
  document.getElementById('wechatCopy').addEventListener('click',()=>copyText('AIPMAndy'));
  const initFilters=(containerId,inputId,listId,emptyId)=>{const container=document.getElementById(containerId),input=document.getElementById(inputId),cards=[...document.getElementById(listId).children],empty=document.getElementById(emptyId);let tag='全部';const filter=()=>{const q=input.value.trim().toLocaleLowerCase('zh-CN');let visible=0;cards.forEach(card=>{const found=(tag==='全部'||card.dataset.tag===tag)&&(!q||card.dataset.search.toLocaleLowerCase('zh-CN').includes(q));card.hidden=!found;if(found)visible++;});empty.hidden=visible!==0;};container.querySelectorAll('button').forEach(btn=>btn.addEventListener('click',()=>{tag=btn.dataset.filter;container.querySelectorAll('button').forEach(b=>{const active=b===btn;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});filter();}));input.addEventListener('input',filter);};
  initFilters('lessonFilters','lessonSearch','lessonList','lessonEmpty');
  initFilters('promptFilters','promptSearch','promptList','promptEmpty');
  let output='';
  document.getElementById('generatePrompt').addEventListener('click',()=>{const goal=document.getElementById('genGoal').value.trim(),outcome=document.getElementById('genOutcome').value.trim(),rules=document.getElementById('genRules').value.trim();if(!goal||!outcome||!rules){notify('先填写目标、验收和限制条件');return;}output=`你是负责项目交付的工程师。请遵循“先审查、再规划、最小改动、执行验证、回顾交付”的流程。\n\n【1. 用户与目标】\n${goal}\n\n【2. 验收标准】\n${outcome}\n\n【3. 限制与禁止动作】\n${rules}\n\n【4. 输入与输出】\n先盘点当前目录与已有依赖，列出实际会读写的文件，并补充我尚未说明的输入输出。\n\n【5. 执行规则】\n在我确认前只读分析，不执行未知脚本、联网、删除、提交、发布或接触秘密。每次只修改明确相关文件，给出可审查 diff。\n\n【6. 交付与证明】\n提供启动命令、测试步骤、实际执行结果、截图/日志证据、未验证项与回滚方法。如果条件不足，停止并说明缺失信息。`;document.getElementById('genOutput').textContent=output;document.getElementById('genResult').hidden=false;notify('已生成任务书');});
  document.getElementById('copyGenerated').addEventListener('click',()=>output&&copyText(output));
  const toggle=document.getElementById('menuToggle'),menu=document.getElementById('mobileNav');toggle.addEventListener('click',()=>{const opened=toggle.getAttribute('aria-expanded')==='true';toggle.setAttribute('aria-expanded',String(!opened));menu.hidden=opened;toggle.setAttribute('aria-label',opened?'打开导航菜单':'关闭导航菜单');});menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{menu.hidden=true;toggle.setAttribute('aria-expanded','false');}));
  // No analytics, API requests, cookies, or remote storage in this site.
})();
