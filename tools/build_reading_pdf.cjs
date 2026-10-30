const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const root = path.resolve(__dirname, '..');
const runtime = 'C:/Users/Logan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium} = require(runtime + '/playwright');
const katex = require(path.join(root, 'tmp/pdfs/node_modules/katex'));
const source = path.join(root, 'translation_draft');
const work = path.join(root, 'tmp/pdfs/faithfulness-20261029/build');
fs.mkdirSync(work, {recursive:true});
const checkOnly = process.argv.includes('--check-only');
const selected = process.argv.find(x => x.startsWith('--section='))?.split('=')[1];
const exportOnly = process.argv.includes('--export-only');
const read = name => fs.readFileSync(path.join(source, name), 'utf8').replace(/^\uFEFF/, '');
function clean(md) {
  return md.split('\n').filter(line => !/^(?:>\s*)?(?:来源[：:]|原文[：:]\s*PDF|原书\s*PDF|原著：.*对应\s*PDF|对应(?:原书|PDF|[：:])|状态：|本整合稿|图像引用|\*\*源文件范围)/.test(line))
    .join('\n').replace(/<!--\s*PDF[\s\S]*?-->/g, '');
}
const front = read('96_front_matter.zh-CN.md');
const slice = (from, to) => front.slice(front.indexOf('<!-- PDF '+from+' '), to ? front.indexOf('<!-- PDF '+to+' ') : undefined);
const sections = [
  {name:'cover', md:slice(1,2), cover:true},
  {name:'title', md:slice(2,3), cover:true},
  {name:'title_third', md:slice(3,7), cover:true},
  {name:'preface', md:read('00_preface.zh-CN.md')},
  {name:'contents', md:slice(7,11), toc:true},
  {name:'student', md:slice(11)},
  {name:'front_tables', md:read('97_front_formula_tables.zh-CN.md')},
];
for (const name of fs.readdirSync(source).filter(n=>n.endsWith('.zh-CN.md')).sort()) {
  if (/^(00_|96_|97_)/.test(name)) continue;
  sections.push({name:name.replace('.zh-CN.md',''), file:name, md:read(name)});
}
const css = `@page{size:A4;margin:19mm 17mm 19mm}*{box-sizing:border-box}body{font-family:'Microsoft YaHei','SimSun',serif;font-size:10.5pt;line-height:1.75;color:#18212b;margin:0}h1{font-size:23pt;line-height:1.4;color:#14374a;margin:0 0 18pt}h2{font-size:16pt;line-height:1.4;color:#14374a;margin:20pt 0 10pt}h3{font-size:12pt;margin:15pt 0 8pt}h4{font-size:11pt;margin:12pt 0 7pt}h1,h2,h3,h4{break-after:avoid}p{margin:7pt 0;orphans:3;widows:3}figure{margin:10pt 0;break-inside:avoid}img{display:block;max-width:100%;max-height:190mm;width:auto;height:auto;margin:0 auto}figcaption{font-size:9pt;line-height:1.6;text-align:center;margin-top:5pt}table{border-collapse:collapse;max-width:100%;width:100%;font-size:9pt;table-layout:auto;margin:10pt 0}th,td{border:0.5pt solid #b6c2c9;padding:5pt 6pt;overflow-wrap:anywhere}th{background:#edf2f4;text-align:left}tr{break-inside:avoid}thead{display:table-header-group}blockquote{margin:12pt 0;padding:8pt 12pt;border-left:3pt solid #37667c;background:#f3f6f7}ul,ol{padding-left:24pt}ol>li::marker{content:counter(list-item) ') '}li{margin:4pt 0;orphans:2;widows:2}a{color:inherit;text-decoration:none}code,pre{font-family:Consolas,'Microsoft YaHei';font-size:9pt;white-space:pre-wrap;overflow-wrap:anywhere}hr{border:0;border-top:0.5pt solid #d5dde1;margin:16pt 0}.katex{font-size:1.04em}.katex-display{margin:10pt 0;break-inside:avoid;text-align:center}.mathblock{max-width:100%;break-inside:avoid;overflow:visible}.cover{height:245mm;display:flex;flex-direction:column;justify-content:center;text-align:center}.cover p{font-size:16pt;line-height:2.5}.katex .mord.text{font-family:'Microsoft YaHei',serif}.footnotes{font-size:9pt;border-top:.5pt solid #b6c2c9;margin-top:18pt;padding-top:6pt}.footnote-ref{font-size:75%;vertical-align:super}`;
const errors = [];
function exportManuscript() {
  const directory=path.join(root,'output/markdown');
  fs.mkdirSync(directory,{recursive:true});
  const manuscript=sections.map(section=>clean(section.md).trim().replace(/(!\[[^\]]*\]\()figures\//g,'$1../../translation_draft/figures/')).join('\n\n')+'\n';
  fs.writeFileSync(path.join(directory,'GilbertStrang-Calculus.md'),manuscript);
}
async function main() {
  if(exportOnly){exportManuscript();return;}
  const {marked} = await import(pathToFileURL(runtime+'/marked/lib/marked.esm.js'));
  const browser = await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true,chromiumSandbox:true});
  const page = await browser.newPage({viewport:{width:665,height:1100}});
  const manifest = [];
  for (let index=0; index<sections.length; index++) {
    const section = sections[index];
    if (selected && section.name !== selected) continue;
    let md = clean(section.md), math = [], footnotes = [];
    if (/^#{1,6}\s*译注|^>\s*译注[：:]/m.test(md)) throw new Error('Unreviewed translator note: '+section.name);
    md = md.replace(/^\[\^([^\]]+)\]:\s*(.*(?:\n(?: {2,}|\t).*)*)/gm, (_,id,body)=>{footnotes.push({id,body});return '';});
    const render = (tex, display) => {
      tex = tex.replace(/^> ?/gm,'').trim().replace(/(?<!\\)_{2,}/g,m=>'\\_'.repeat(m.length));
      tex = tex.replace('\\multicolumn{5}{c}{\\text{二项式系数}}','\\text{二项式系数}');
      const key = 'MATHPLACEHOLDER'+math.length+'END';
      try {const html = katex.renderToString(tex,{displayMode:display,throwOnError:true,strict:'ignore',output:'html',maxExpand:2000});math.push(display?'<div class="mathblock">'+html+'</div>':html);}
      catch(e) {errors.push({section:section.name,tex,error:e.message});math.push('<span class="math-error">'+tex.replace(/</g,'&lt;')+'</span>');}
      return key;
    };
    if (footnotes.length) {
      md = md.replace(/\[\^([^\]]+)\]/g,(_,id)=>{const n=footnotes.findIndex(f=>f.id===id);if(n<0)throw new Error('Missing footnote '+id);return '<sup class="footnote-ref">'+(n+1)+'</sup>';});
      md += '\n\n<div class="footnotes">\n\n'+footnotes.map((f,i)=>'**'+(i+1)+'** '+f.body).join('\n\n')+'\n\n</div>\n';
    }
    md = md.replace(/(^[ \t]*(?:> ?)*|)\$\$([\s\S]*?)\$\$/gm,(_,prefix,tex)=>{
      const block=render(tex,true);
      return prefix.includes('>')?'\n'+prefix+'\n'+prefix+block+'\n'+prefix:'\n\n'+prefix+block+'\n\n';
    });
    md = md.replace(/(?<!\\)\$([^\n$]+?)(?<!\\)\$/g,(_,tex)=>render(tex,false));
    md = md.replace(/(?<!\\)_{2,}/g,blank=>blank.replace(/_/g,'\\_'));
    md = md.replace(/\*\*([^\n]+?)\*\*/g,'<strong>$1</strong>');
    let html = marked.parse(md,{gfm:true});
    // Alt descriptions are not extra captions. / 替代文本不自动增作图注。
    html = html.replace(/<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*\/?>/g,(match,src,caption,offset,whole)=>{
      const figure = caption.match(/^图\s*(\d+\.\d+)\s*[:：]?\s*(.*)$/);
      const following = whole.slice(offset+match.length).replace(/^\s*<\/p>/,'').trimStart();
      const nextFigure = following.match(/^<p>\s*(?:<strong>)?图\s*(\d+\.\d+)/);
      const onlyCaption = figure && figure[2] && nextFigure?.[1] !== figure[1];
      return '<figure><img src="'+src+'" alt="'+caption+'">'+(onlyCaption?'<figcaption>'+caption+'</figcaption>':'')+'</figure>';
    });
    html = html.replace(/MATHPLACEHOLDER(\d+)END/g,(_,n)=>math[+n]);
    html = html.replace(/src="([^"]+)"/g,(_,src)=>'src="'+pathToFileURL(path.isAbsolute(decodeURI(src))?decodeURI(src):path.resolve(source,decodeURI(src))).href+'"');
    const htmlFile = path.join(work,String(index).padStart(3,'0')+'.html');
    fs.writeFileSync(htmlFile,'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><link rel="stylesheet" href="'+pathToFileURL(path.join(root,'tmp/pdfs/node_modules/katex/dist/katex.min.css')).href+'"><style>'+css+'</style><body class="'+(section.cover?'cover':'')+'">'+html+'</body></html>');
    await page.goto(pathToFileURL(htmlFile).href,{waitUntil:'load'});
    await page.evaluate(()=>document.fonts.ready);
    const layout = await page.evaluate(({index,toc})=>{
      // Keep the original caption with its image. / 原图注与图片共同分页。
      for(const figure of document.querySelectorAll('figure')) {
        if(figure.querySelector('figcaption'))continue;
        const number=figure.querySelector('img')?.alt.match(/^图\s*(\d+(?:\.\d+)?|[A-Z])/i)?.[1];
        if(!number)continue;
        let next=figure.nextElementSibling;
        while(next?.tagName==='P'&&!next.textContent.trim()&&!next.children.length)next=next.nextElementSibling;
        if(next?.tagName==='P'&&next.textContent.trim().match(/^图\s*(\d+(?:\.\d+)?|[A-Z])/i)?.[1]===number) {
          const caption=document.createElement('figcaption');caption.innerHTML=next.innerHTML;
          figure.append(caption);next.remove();
        }
      }
      for(const p of document.querySelectorAll('p')) {
        if(p.nextElementSibling?.classList.contains('mathblock')&&p.querySelector('strong'))p.style.breakAfter='avoid';
      }
      const headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map((el,n)=>{
        const id='s'+index+'h'+n, title=el.textContent.replace(/\s+/g,' ').trim(), level=+el.tagName.slice(1);
        const a=document.createElement('a');a.href='https://calculus.invalid/heading/'+id;
        while(el.firstChild)a.append(el.firstChild);el.append(a);return {id,title,level};
      });
      if(toc)for(const row of document.querySelectorAll('tbody tr')) {
        const token=row.cells[0]?.textContent.trim(), chapter=token?.match(/^第(\d+)章$/);
        const key=chapter?'ch'+chapter[1]:/^\d+\.\d+$/.test(token)?token:null;
        if(key)for(const cell of row.cells){const a=document.createElement('a');a.href='https://calculus.invalid/target/'+key;while(cell.firstChild)a.append(cell.firstChild);cell.append(a);}
      }
      let scaled=0;
      for(const el of document.querySelectorAll('.mathblock')) {
        const inner=el.querySelector('.katex-html');
        const w=[...(inner?.querySelectorAll(':scope>.base')||[])].reduce((s,b)=>s+b.getBoundingClientRect().width,0)+(inner?.querySelector('.tag')?.getBoundingClientRect().width||0);
        const available=el.clientWidth-4;
        if(w>available){el.style.fontSize=(available/w*100)+'%';scaled++;}
      }
      const badImages=[...document.images].filter(img=>!img.complete||!img.naturalWidth).map(img=>img.src);
      const overflow=[...document.querySelectorAll('table,.mathblock,figure,p,pre')].filter(el=>el.scrollWidth>el.clientWidth+3).map(el=>({tag:el.tagName,text:el.textContent.slice(0,80),width:el.scrollWidth,available:el.clientWidth}));
      return {headings,scaled,badImages,overflow};
    },{index,toc:section.toc||false});
    if(layout.badImages.length)throw new Error('Missing images: '+JSON.stringify(layout.badImages));
    const pdf = path.join(work,String(index).padStart(3,'0')+'.pdf');
    if(!checkOnly)await page.pdf({path:pdf,format:'A4',printBackground:true,preferCSSPageSize:true});
    manifest.push({index,name:section.name,file:section.file,pdf,layout});
    if(index%5===0)console.log(JSON.stringify({completed:index+1,total:sections.length,mathErrors:errors.length,overflow:layout.overflow.length}));
  }
  await browser.close();
  fs.writeFileSync(path.join(work,'math_errors'+(selected?'-'+selected:'')+'.json'),JSON.stringify(errors,null,2));
  fs.writeFileSync(path.join(work,'manifest'+(selected?'-'+selected:'')+'.json'),JSON.stringify(manifest,null,2));
  console.log(JSON.stringify({complete:manifest.length,mathErrors:errors.length,checkOnly}));
  if(!checkOnly&&!selected&&!errors.length)exportManuscript();
  if(errors.length)process.exitCode=2;
}
main().catch(e=>{console.error(e);process.exitCode=1;});
