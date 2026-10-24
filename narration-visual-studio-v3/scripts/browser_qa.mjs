#!/usr/bin/env node
/** Local-only evidence capture. The artwork timeline is always sought, never wall-clock played. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {spawnSync} from 'node:child_process';
import {chromium} from 'playwright';
import sharp from 'sharp';

const project = path.resolve(process.argv[2] || '');
const result = spawnSync('python3', [path.join(import.meta.dirname, 'audit_project.py'), project], {encoding:'utf8'});
if (result.status !== 0) throw new Error(`Project audit failed: ${result.stdout}\n${result.stderr}`);
const audit = JSON.parse(result.stdout);
const review = path.join(project,'review');
await fs.mkdir(path.join(review,'all'), {recursive:true});
const browser = await chromium.launch({channel:'chrome', headless:true});
const report = {status:'NEEDS_VISUAL_REVIEW', errors:[], warnings:[], resolutions:[], deterministic:[]};
const shots = [];
try {
  for (const width of [1920,1280]) {
    const page = await browser.newPage({viewport:{width,height:width*9/16},deviceScaleFactor:1});
    await page.route('**/*', route => /^https?:/.test(route.request().url()) ? route.abort() : route.continue());
    page.on('pageerror', e => report.errors.push(`JS: ${e.message}`));
    await page.goto(pathToFileURL(path.join(project,'index.html')).href, {waitUntil:'load'});
    await page.evaluate(()=>document.fonts.ready);
    await page.waitForFunction(()=>window.nvs?.seek);
    for (const t of audit.sample_times) {
      await page.evaluate(t=>window.nvs.seek(t),t);
      const findings = await page.evaluate(()=>{
        const root=document.querySelector('[data-composition-id]');
        const rb=root.getBoundingClientRect();
        const visible=e=>{for(let n=e;n;n=n.parentElement){const s=getComputedStyle(n);if(s.visibility==='hidden'||s.display==='none'||Number(s.opacity)<.05)return false;}return true;};
        const issues=[];
        const clips=[...root.querySelectorAll('.clip')].filter(visible);
        if(clips.length!==1)issues.push(`visible-scene-count: ${clips.length}`);
        for(const e of root.querySelectorAll('h1,h2,h3,p,li,figcaption,svg text,[data-qa-text]')){
          if(!visible(e))continue;
          const b=e.getBoundingClientRect();
          if(!b.width||!b.height)continue;
          if(b.left<rb.left-3||b.top<rb.top-3||b.right>rb.right+3||b.bottom>rb.bottom+3)issues.push(`outside-stage: ${e.textContent.slice(0,55)}`);
          if(e.scrollWidth>e.clientWidth+3&&e.clientWidth>0)issues.push(`text-overflow: ${e.textContent.slice(0,55)}`);
        }
        for(const e of root.querySelectorAll('img'))if(!e.complete||!e.naturalWidth)issues.push(`broken-image: ${e.getAttribute('src')}`);
        for(const e of root.querySelectorAll('video'))if(e.error)issues.push(`broken-video: ${e.getAttribute('src')}`);
        if(rb.left< -3||rb.top< -3||rb.right>innerWidth+3||rb.bottom>innerHeight+3)issues.push('stage-outside-viewport');
        return issues;
      });
      report.errors.push(...findings.map(x=>`${width}px @${t}s ${x}`));
      const filename=`${width}-${String(t).replace('.','_')}.png`;
      await page.screenshot({path:path.join(review,'all',filename)});
      if(width===1920)shots.push({t,file:filename});
    }
    // Compare identical time after arbitrary forward/backward navigation, on the same page.
    for(const t of [audit.duration*.13,audit.duration*.51,audit.duration-.04,audit.duration]){
      await page.evaluate(t=>window.nvs.seek(t),t);
      const first=await page.screenshot();
      await page.evaluate(t=>{window.nvs.seek(t*.3);window.nvs.seek(t+0.001);window.nvs.seek(t);},t);
      const second=await page.screenshot();
      const stable=first.equals(second);
      report.deterministic.push({width,time:t,stable});
      if(!stable)report.errors.push(`non-deterministic seek ${width}px @${t}`);
    }
    report.resolutions.push({width,height:width*9/16,samples:audit.sample_times.length,network:'blocked / system font fallback'});
    await page.close();
  }
} finally { await browser.close(); }
// One retained representative frame per scene, all precise states remain locally in review/all.
const sceneData=JSON.parse(await fs.readFile(path.join(project,'scenes.json'),'utf8'));
const scenes=Array.isArray(sceneData)?sceneData:sceneData.scenes;
const tiles=[];
for(let i=0;i<scenes.length;i++){
 const scene=scenes[i]; const target=scene.end-.04;
 const shot=shots.reduce((a,b)=>Math.abs(a.t-target)<Math.abs(b.t-target)?a:b);
 const filename=`scene-${String(i+1).padStart(2,'0')}.png`;
 await fs.copyFile(path.join(review,'all',shot.file),path.join(review,filename));
 const image=await sharp(path.join(review,filename)).resize(640,360).png().toBuffer();
 tiles.push({input:image,left:(i%2)*640,top:Math.floor(i/2)*360});
}
await sharp({create:{width:1280,height:Math.ceil(tiles.length/2)*360,channels:3,background:'#ddd'}}).composite(tiles).png().toFile(path.join(review,'contact-sheet.png'));
await fs.writeFile(path.join(review,'screenshot-index.json'),JSON.stringify({samples:shots,retained:scenes.map((s,i)=>({scene_id:s.scene_id,file:`scene-${String(i+1).padStart(2,'0')}.png`,time:s.end-.04}))},null,2));
report.status=report.errors.length?'BLOCKED':'NEEDS_VISUAL_REVIEW';
await fs.writeFile(path.join(review,'browser-qa.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify(report,null,2));
process.exitCode=report.errors.length?1:0;
