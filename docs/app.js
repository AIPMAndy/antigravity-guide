'use strict';
(() => {
  const STORAGE = 'andy-antigravity-guide-progress-v1';
  const items = [...document.querySelectorAll('input[data-key]')];
  const dayCount = document.querySelectorAll('.day-checkbox').length;
  const lessonCount = document.querySelectorAll('.lesson-checkbox').length;
  const toast = document.getElementById('toast');
  let noticeTimer = null;
  const notify = (message) => { toast.textContent = message; toast.classList.add('show'); clearTimeout(noticeTimer); noticeTimer = setTimeout(()=>toast.classList.remove('show'), 2800); };
  const undoButton=document.getElementById('undoProgress'),resetButton=document.getElementById('resetProgress');
  let undoState=null;
  const currentState = () => Object.fromEntries(items.map(x => [x.dataset.key, x.checked]));
  const saveState=()=>{try{localStorage.setItem(STORAGE,JSON.stringify(currentState()));return true;}catch{return false;}};
  const setUndo=state=>{undoState=state;undoButton.hidden=state===null;};
  const replaceProgress=(next,message)=>{setUndo(currentState());applyState(next);notify(saveState()?message+'，可撤销。':message+'，但本机保存失败，请导出备份。');};
  const applyState = state => { items.forEach(x => {x.checked = state[x.dataset.key] === true;}); drawProgress(); };
  const drawProgress = () => {
    const done = items.filter(x=>x.checked).length;
    const percent = Math.round(100 * done / items.length);
    document.getElementById('progressRing').style.background = `conic-gradient(#3c6cf3 ${percent*3.6}deg,#e8eefb 0deg)`;
    document.getElementById('progressValue').textContent = percent + '%';
    document.getElementById('progressRing').setAttribute('aria-valuenow', String(percent));
    resetButton.disabled=done===0;
    document.getElementById('progressSubtitle').textContent = `${done} / ${items.length} 项已完成（${dayCount} 天 + ${lessonCount} 章）`;
  };
  try {const saved=JSON.parse(localStorage.getItem(STORAGE) || '{}'); if(saved && typeof saved==='object' && !Array.isArray(saved)) applyState(saved);} catch {notify('浏览器本地进度不可读取；仍可手动打卡并导出');}
  items.forEach(box=>box.addEventListener('change',()=>{setUndo(null);drawProgress();if(!saveState())notify('当前浏览器无法保存，建议手动导出进度');}));
  undoButton.addEventListener('click',()=>{if(undoState===null)return;const state=undoState;setUndo(null);applyState(state);notify(saveState()?'已撤销上次进度修改':'已恢复当前界面，保存失败，请导出备份');(resetButton.disabled?document.getElementById('exportProgress'):resetButton).focus({preventScroll:true});});
  drawProgress();
  const downloadText = (name,body,type) => {const blob=new Blob([body],{type});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1500);};
  document.getElementById('exportProgress').addEventListener('click',()=>{downloadText('antigravity-progress.json',JSON.stringify({version:1,exportedAt:new Date().toISOString(),checked:currentState()},null,2),'application/json;charset=utf-8');notify('进度文件已导出');});
  document.getElementById('importProgress').addEventListener('click',()=>document.getElementById('progressFile').click());
  document.getElementById('progressFile').addEventListener('change',async e=>{
    const file=e.target.files?.[0];if(!file)return;
    try{
      if(file.size>100000)throw Error('文件过大');
      const parsed=JSON.parse(await file.text());
      if(parsed?.version!==1||!parsed.checked||typeof parsed.checked!=='object'||Array.isArray(parsed.checked))throw Error('格式不匹配');
      const keys=new Set(items.map(x=>x.dataset.key)),safe={};
      for(const [k,v] of Object.entries(parsed.checked)){if(keys.has(k)){if(typeof v!=='boolean')throw Error('非布尔型进度');safe[k]=v;}}
      if(!Object.keys(safe).length)throw Error('没有可识别的课程进度');
      if(items.some(x=>x.checked)&&!confirm('导入将替换当前学习进度。是否继续？导入后可撤销。')){notify('未替换现有学习进度');return;}
      replaceProgress(safe,'进度已导入');
    }catch(err){notify('导入失败：'+err.message);}finally{e.target.value='';}
  });
  resetButton.addEventListener('click',()=>{if(!items.some(x=>x.checked))return;if(!confirm('清空当前学习打卡？清空后可立即撤销，不会删除项目文件。'))return;replaceProgress({},'本机打卡已清空');undoButton.focus({preventScroll:true});});
  async function copyText(text){try{if(navigator.clipboard?.writeText && window.isSecureContext){await navigator.clipboard.writeText(text);}else{const field=document.createElement('textarea');field.value=text;field.setAttribute('readonly','');field.style.position='fixed';field.style.left='-9999px';document.body.append(field);field.select();const ok=document.execCommand('copy');field.remove();if(!ok)throw Error('请手动复制');}notify('已复制到剪贴板');}catch{notify('复制失败，请选择文本手动复制');}}
  document.querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',()=>copyText(button.dataset.copy)));
  document.getElementById('wechatCopy').addEventListener('click',()=>copyText('AIPMAndy'));
  const initFilters=prefix=>{
    const container=document.getElementById(prefix+'Filters'),input=document.getElementById(prefix+'Search'),
      cards=[...document.getElementById(prefix+'List').children],empty=document.getElementById(prefix+'Empty'),
      count=document.getElementById(prefix+'Count'),reset=document.getElementById(prefix+'Reset');
    const buttons=[...container.querySelectorAll('button')];let tag='全部';
    const syncTag=()=>buttons.forEach(b=>{const active=b.dataset.filter===tag;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});
    const filter=()=>{const q=input.value.trim().toLocaleLowerCase('zh-CN');let visible=0;
      cards.forEach(card=>{const found=(tag==='全部'||card.dataset.tag===tag)&&(!q||card.dataset.search.toLocaleLowerCase('zh-CN').includes(q));card.hidden=!found;if(found)visible++;});
      empty.hidden=visible!==0;const label=visible+' / '+cards.length+' 项';if(count.textContent!==label)count.textContent=label;reset.hidden=!q&&tag==='全部';};
    buttons.forEach(btn=>btn.addEventListener('click',()=>{tag=btn.dataset.filter;syncTag();filter();}));
    input.addEventListener('input',filter);
    reset.addEventListener('click',()=>{tag='全部';input.value='';syncTag();filter();input.focus({preventScroll:true});});
    filter();
  };
  initFilters('lesson');initFilters('prompt');
  let output='',snapshot='';
  const fields=['genGoal','genOutcome','genRules'].map(id=>document.getElementById(id));
  const result=document.getElementById('genResult'),copyGenerated=document.getElementById('copyGenerated'),status=document.getElementById('genStatus');
  const signature=()=>JSON.stringify(fields.map(x=>x.value.trim()));
  const showStatus=message=>{status.textContent=message;status.hidden=!message;};
  const invalidate=()=>{output='';snapshot='';copyGenerated.disabled=true;result.hidden=true;document.getElementById('genOutput').textContent='';};
  fields.forEach(field=>field.addEventListener('input',()=>{if(output&&signature()!==snapshot){invalidate();showStatus('输入已修改，请重新生成任务书。');}}));
  document.getElementById('generatePrompt').addEventListener('click',()=>{const goal=document.getElementById('genGoal').value.trim(),outcome=document.getElementById('genOutcome').value.trim(),rules=document.getElementById('genRules').value.trim();if(!goal||!outcome||!rules){invalidate();showStatus('请补齐目标、验收和限制条件。');fields.find(x=>!x.value.trim())?.focus({preventScroll:true});return;}output=`你是负责项目交付的工程师。请遵循“先审查、再规划、最小改动、执行验证、回顾交付”的流程。\n\n【1. 用户与目标】\n${goal}\n\n【2. 验收标准】\n${outcome}\n\n【3. 限制与禁止动作】\n${rules}\n\n【4. 输入与输出】\n先盘点当前目录与已有依赖，列出实际会读写的文件，并补充我尚未说明的输入输出。\n\n【5. 执行规则】\n在我确认前只读分析，不执行未知脚本、联网、删除、提交、发布或接触秘密。每次只修改明确相关文件，给出可审查 diff。\n\n【6. 交付与证明】\n提供启动命令、测试步骤、实际执行结果、截图/日志证据、未验证项与回滚方法。如果条件不足，停止并说明缺失信息。`;snapshot=signature();document.getElementById('genOutput').textContent=output;result.hidden=false;copyGenerated.disabled=false;showStatus('任务书已生成，可复制。');});
  copyGenerated.addEventListener('click',()=>{if(!output||signature()!==snapshot){invalidate();showStatus('输入已修改，请重新生成任务书。');return;}copyText(output);});
  const toggle=document.getElementById('menuToggle'),menu=document.getElementById('mobileNav');
  const setMenu=open=>{menu.hidden=!open;toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'关闭导航菜单':'打开导航菜单');};
  toggle.addEventListener('click',()=>setMenu(menu.hidden));
  menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!menu.hidden){setMenu(false);toggle.focus({preventScroll:true});}});
  if(window.matchMedia){window.matchMedia('(min-width:781px)').addEventListener('change',event=>{if(event.matches)setMenu(false);});}
  // No analytics, API requests, cookies, or remote storage in this site.
})();
