# -*- coding: utf-8 -*-
"""Лендинг класса 10-Л — один файл, данные те же, что в книге."""
import os, sys, json
ЗДЕСЬ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ЗДЕСЬ)
from data import LESSON_TIMES, INTERVALS, FAMILY, WEEK
from marks import svg_sunc, svg_ring

OUT = os.path.join(ЗДЕСЬ, 'out', 'index.html')

payload = {
    'lessons': {str(k): list(v) for k, v in LESSON_TIMES.items()},
    'intervals': [{'kind': k, 'name': n, 'a': a, 'b': b} for k, n, a, b in INTERVALS],
    'family': {k: {'color': v[0], 'title': v[1]} for k, v in FAMILY.items()},
    'week': [{'name': d[0], 'short': d[1],
              'blocks': [{'l0': b[0], 'l1': b[1], 'fam': b[2], 'name': b[3],
                          'note': b[4], 'teacher': b[5], 'room': b[6]} for b in d[2]]}
             for d in WEEK],
}

HTML = r"""<!doctype html>
<html lang="ru"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>10-Л · химический класс · СУНЦ МГУ</title>
<meta name="description" content="Расписание уроков 10-Л, СУНЦ МГУ. I семестр 2026/27.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@600;800&family=Manrope:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{
  --ink:#0A0D13; --up:#11161F; --line:#1E2635;
  --paper:#EEF2F8; --amber:#FFC53D; --chem:#FF5C93;
  --muted:#66748C; --muted2:#3F4A5D;
  --disp:'Unbounded',system-ui,sans-serif;
  --sans:'Manrope',system-ui,sans-serif;
  --mono:'JetBrains Mono',ui-monospace,monospace;
  --pad:clamp(18px,4vw,64px);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--ink);color:var(--paper);font-family:var(--sans);
     overflow-x:hidden}
.wrap{max-width:1360px;margin:0 auto;padding:0 var(--pad)}
.micro{font-family:var(--mono);font-size:10px;letter-spacing:.22em;color:var(--muted2);
       text-transform:uppercase}
.micro.b{color:var(--muted)}
.rule{height:1px;background:var(--muted2);opacity:.5}
h2.sec{font-family:var(--disp);font-weight:800;font-size:clamp(26px,4.4vw,50px);
       letter-spacing:.03em;margin:0}
section{padding:clamp(46px,7vw,104px) 0}

/* молекулярный фон */
.mesh{position:fixed;inset:0;z-index:0;pointer-events:none;opacity:.5}
.mesh svg{width:200%;height:200%;animation:drift 90s linear infinite}
@keyframes drift{to{transform:translate(-72px,-124.7px)}}
.glow{position:fixed;z-index:0;pointer-events:none;filter:blur(90px);opacity:.30;
      border-radius:50%}
.g1{width:44vw;height:44vw;background:var(--chem);top:-14vw;right:-10vw}
.g2{width:38vw;height:38vw;background:#2BD576;top:52vw;left:-14vw}
main,header{position:relative;z-index:1}

/* шапка */
header{position:sticky;top:0;backdrop-filter:blur(14px);
       background:rgba(10,13,19,.78);border-bottom:1px solid var(--line);z-index:20}
.nav{display:flex;align-items:center;gap:18px;padding:12px var(--pad);max-width:1360px;
     margin:0 auto}
.nav .sunc{display:flex;align-items:center;gap:10px}
.nav .sunc svg{width:30px;height:auto;display:block}
.nav .sunc b{font-family:var(--mono);font-size:10px;letter-spacing:.2em;font-weight:700}
.nav .sunc i{font-style:normal;display:block;font-family:var(--mono);font-size:8.5px;
             letter-spacing:.14em;color:var(--muted2)}
.nav .sp{flex:1}
.nav a{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;
       color:var(--muted);text-decoration:none;transition:color .2s}
.nav a:hover{color:var(--paper)}
@media (max-width:760px){.nav a.hide{display:none}}

/* герой */
.hero{padding:clamp(40px,7vw,92px) 0 clamp(30px,4vw,50px)}
.lock{display:flex;align-items:center;gap:clamp(16px,3vw,40px);flex-wrap:wrap}
.lock .ring{width:clamp(96px,13vw,168px);flex:none}
.lock .ring path{stroke-dasharray:120;stroke-dashoffset:120;
                 animation:draw 1.1s cubic-bezier(.2,.85,.25,1) forwards}
.lock .ring circle{stroke-dasharray:400;stroke-dashoffset:400;
                   animation:draw 1.4s .35s cubic-bezier(.2,.85,.25,1) forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.lock .ring path:nth-child(1){animation-delay:.05s}
.lock .ring path:nth-child(2){animation-delay:.13s}
.lock .ring path:nth-child(3){animation-delay:.21s}
.lock .ring path:nth-child(4){animation-delay:.29s}
.lock .ring path:nth-child(5){animation-delay:.37s}
.lock .ring path:nth-child(6){animation-delay:.45s}
.mark{font-family:var(--disp);font-weight:800;font-size:clamp(64px,12vw,168px);
      line-height:.84;letter-spacing:-.03em;margin:0}
.mark span{display:inline-block;opacity:0;transform:translateY(.3em);
           animation:rise .8s cubic-bezier(.2,.9,.2,1) forwards}
@keyframes rise{to{opacity:1;transform:none}}
.kicker{font-family:var(--mono);font-size:clamp(10px,1.2vw,13px);letter-spacing:.42em;
        color:var(--chem);margin:0 0 10px}
.claim{font-family:var(--disp);font-weight:600;font-size:clamp(20px,3.4vw,42px);
       letter-spacing:.04em;margin:clamp(26px,4vw,52px) 0 0;color:var(--amber)}
.claim em{font-style:normal;color:#8A93A6;display:block}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1px;
       background:var(--line);border:1px solid var(--line);border-radius:6px;
       overflow:hidden;margin-top:clamp(26px,4vw,46px)}
.stats div{background:var(--up);padding:18px 20px}
.stats b{font-family:var(--disp);font-weight:800;font-size:clamp(22px,3vw,34px);display:block}
.stats span{display:block;margin-top:6px}

/* спектр */
.spectrum{display:grid;grid-template-columns:34px repeat(6,1fr);gap:clamp(5px,1vw,12px)}
.hours{position:relative;height:var(--sh)}
.hours i{position:absolute;right:0;transform:translateY(-50%);font-family:var(--mono);
         font-size:9px;color:var(--muted2);font-style:normal}
.col{position:relative;height:var(--sh);background:var(--up);border:0;padding:0;
     cursor:pointer;overflow:hidden;border-radius:4px;transition:filter .3s,transform .3s}
.col:hover{filter:brightness(1.25);transform:translateY(-3px)}
.col u{position:absolute;left:0;right:0;height:1px;background:rgba(238,242,248,.07)}
.col b{position:absolute;left:0;right:0;border-radius:3px;transform:scaleY(0);
       transform-origin:top}
.col.lit b{transform:none;transition:transform .7s cubic-bezier(.2,.85,.25,1)}
.col.on{outline:2px solid var(--paper);outline-offset:2px}
.caps{display:grid;grid-template-columns:34px repeat(6,1fr);gap:clamp(5px,1vw,12px);
      margin-top:12px}
.caps .d{text-align:center;font-family:var(--mono);font-size:10px;letter-spacing:.16em;
         color:var(--muted)}
.caps .n{text-align:center;font-family:var(--mono);font-size:9px;letter-spacing:.14em;
         color:var(--muted2);margin-top:4px}

/* день */
.dayhead{display:flex;flex-wrap:wrap;align-items:baseline;gap:20px;margin:22px 0 14px}
.dayname{font-family:var(--disp);font-weight:800;font-size:clamp(26px,4.6vw,50px);
         letter-spacing:.03em;margin:0}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 22px}
.bar button{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;
            background:var(--up);color:var(--muted);border:1px solid var(--line);
            border-radius:4px;padding:9px 14px;cursor:pointer;transition:.2s}
.bar button:hover{color:var(--paper);border-color:var(--muted2)}
.bar button.on{background:var(--paper);color:var(--ink);border-color:var(--paper)}
.bar .sp{flex:1}
.tl{position:relative;height:var(--th);margin-left:32px}
.tl .hr{position:absolute;left:-32px;right:0;height:1px;background:rgba(238,242,248,.08)}
.tl .hr i{position:absolute;left:-32px;top:-6px;font-family:var(--mono);font-size:9px;
          color:var(--muted2);font-style:normal}
.tl .meal{position:absolute;left:0;right:0;background:rgba(255,197,61,.11);border-radius:3px}
.tl .meal span{position:absolute;right:9px;top:50%;transform:translateY(-50%);
           font-family:var(--mono);font-size:9px;letter-spacing:.18em;color:#8A7434}
.blk{position:absolute;left:0;right:0;border-radius:7px;opacity:0;transform:translateX(-24px);
     animation:slide .6s cubic-bezier(.2,.85,.25,1) forwards}
@keyframes slide{to{opacity:1;transform:none}}
.blk .meta{position:absolute;left:2px;top:0;bottom:0;width:124px}
.blk .meta u{position:absolute;left:0;right:0;border-radius:4px;text-decoration:none}
.blk .meta em{position:absolute;font-style:normal;font-family:var(--disp);font-weight:800;
              font-size:15px;left:14px;top:8px}
.blk .meta s{position:absolute;left:42px;top:9px;text-decoration:none;font-family:var(--mono);
             font-size:9.5px;line-height:1.35;white-space:pre}
.blk .body{position:absolute;left:168px;right:20px;top:50%;transform:translateY(-50%);
           display:flex;align-items:center;justify-content:space-between;gap:18px}
.blk .nm{font-weight:800;font-size:clamp(15px,1.9vw,27px)}
.blk .note{font-family:var(--mono);font-size:9.5px;letter-spacing:.18em;margin-left:14px;
           text-transform:uppercase;white-space:nowrap}
.blk .rt{text-align:right;white-space:nowrap}
.blk .room{font-family:var(--mono);font-weight:700;font-size:13px;letter-spacing:.1em}
.blk .room i{font-style:normal;font-size:8px;letter-spacing:.14em;opacity:.6;margin-right:6px}
.blk .tch{font-weight:600;font-size:10.5px;opacity:.72;margin-top:4px}
.free{position:absolute;left:0;right:0;border:1px dashed var(--line);border-radius:7px;
      display:flex;align-items:center;gap:18px;padding:0 16px;color:var(--muted2)}
.free em{font-style:normal;font-family:var(--disp);font-weight:800;font-size:15px}
.free s{text-decoration:none;font-family:var(--mono);font-size:9.5px;letter-spacing:.24em}
.now{position:absolute;left:-32px;right:0;height:1px;background:var(--amber);z-index:4}
.now b{position:absolute;right:0;top:-8px;background:var(--amber);color:#241a00;
       font-family:var(--mono);font-size:9px;font-weight:700;letter-spacing:.12em;
       padding:2px 6px;border-radius:3px}

/* звонки и предметы */
.grid2{display:grid;grid-template-columns:1fr;gap:clamp(30px,5vw,64px)}
@media (min-width:960px){.grid2{grid-template-columns:1.15fr .85fr}}
.brow{display:grid;grid-template-columns:40px 1fr 66px 14px 66px 62px;align-items:center;
      gap:10px;padding:5px 0;font-family:var(--mono);font-size:10px;color:var(--muted2)}
.brow.les{background:var(--up);border-left:3px solid var(--amber);padding:9px 0 9px 11px;
          color:var(--paper);margin:3px 0;border-radius:0 4px 4px 0}
.brow .no{font-family:var(--disp);font-weight:800;font-size:16px}
.brow .nm{font-family:var(--sans);font-weight:800;font-size:12px;letter-spacing:.16em;
          text-transform:uppercase}
.brow.les .t{font-weight:700;font-size:14px}
.brow.eat{color:var(--amber)}
.subj{display:flex;flex-direction:column;gap:9px}
.srow{display:grid;grid-template-columns:16px 1fr 34px 52px;align-items:center;gap:12px}
.srow i{width:16px;height:16px;border-radius:4px;display:block}
.srow .t{font-weight:800;font-size:12.5px;letter-spacing:.06em}
.srow .n{font-family:var(--disp);font-weight:800;font-size:14px;text-align:right}
.srow .h{font-family:var(--mono);font-size:10px;color:var(--muted);text-align:right}
.srow .track{grid-column:1/-1;height:5px;border-radius:3px;background:var(--up);overflow:hidden}
.srow .track b{display:block;height:100%;border-radius:3px;width:0;
               transition:width .9s cubic-bezier(.2,.85,.25,1)}

/* скачать */
.dl{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.dl a{display:block;background:var(--up);border:1px solid var(--line);border-radius:8px;
      padding:22px;text-decoration:none;color:inherit;transition:.25s}
.dl a:hover{border-color:var(--chem);transform:translateY(-3px)}
.dl b{font-family:var(--disp);font-weight:600;font-size:17px;letter-spacing:.03em;display:block}
.dl span{display:block;margin-top:8px}
footer{padding:38px 0 54px;border-top:1px solid var(--line);display:flex;flex-wrap:wrap;
       gap:16px;justify-content:space-between;align-items:center}
footer .sunc svg{width:34px;display:block}
@media (max-width:880px){
  .blk .meta{display:none}.blk .body{left:18px}
  .brow{grid-template-columns:30px 1fr 56px 12px 56px;font-size:9px}
  .brow .du{display:none}
}
@media (prefers-reduced-motion:reduce){
  *{animation:none!important;transition:none!important}
  .mark span,.blk{opacity:1!important;transform:none!important}
  .col b{transform:none!important}
  .lock .ring path,.lock .ring circle{stroke-dashoffset:0!important}
}
</style></head><body>

<div class="mesh">__MESH__</div>
<div class="glow g1"></div><div class="glow g2"></div>

<header><nav class="nav">
  <span class="sunc">__SUNC__<span><b>СУНЦ МГУ</b><i>им. А. Н. Колмогорова</i></span></span>
  <span class="sp"></span>
  <a href="#nedelya" class="hide">Неделя</a>
  <a href="#den">День</a>
  <a href="#zvonki" class="hide">Звонки</a>
  <a href="#pdf">PDF</a>
</nav></header>

<main>
<div class="wrap">

<section class="hero">
  <div class="lock">
    <span class="ring">__RING__</span>
    <div>
      <p class="kicker">ХИМИЧЕСКИЙ КЛАСС</p>
      <p class="mark" id="mark"></p>
    </div>
  </div>
  <p class="claim">НЕДЕЛЯ, КОТОРУЮ ВИДНО<em>расписание I семестра 2026/27</em></p>
  <div class="stats">
    <div><b>38</b><span class="micro b">уроков в неделю</span></div>
    <div><b>6</b><span class="micro b">учебных дней</span></div>
    <div><b>28:30</b><span class="micro b">часов занятий</span></div>
    <div><b>40</b><span class="micro b">свой кабинет</span></div>
  </div>
</section>

<div class="rule"></div>

<section id="nedelya">
  <h2 class="sec">НЕДЕЛЯ</h2>
  <p class="micro b" style="margin:10px 0 26px">Высота полосы равна длительности · нажмите на день</p>
  <div class="spectrum" id="spectrum"></div>
  <div class="caps" id="caps"></div>
</section>

<div class="rule"></div>

<section id="den">
  <p class="micro" style="margin:0 0 6px">День</p>
  <div class="dayhead" style="margin-top:0">
    <h2 class="sec dayname" id="dayname">—</h2>
    <span class="micro b" id="dayfacts"></span>
  </div>
  <div class="bar" id="bar"></div>
  <div class="tl" id="tl"></div>
</section>

<div class="rule"></div>

<section id="zvonki">
  <div class="grid2">
    <div>
      <h2 class="sec">ЗВОНКИ</h2>
      <p class="micro b" style="margin:10px 0 22px">Единая сетка для всех классов</p>
      <div id="bells"></div>
      <p class="micro" style="margin-top:16px">Полдник в источнике начинается в 16:40 —
         за пять минут до конца 8-го урока</p>
    </div>
    <div>
      <h2 class="sec">ПРЕДМЕТЫ</h2>
      <p class="micro b" style="margin:10px 0 22px">Часы за неделю · 1 урок = 45 минут</p>
      <div class="subj" id="subj"></div>
    </div>
  </div>
</section>

<div class="rule"></div>

<section id="pdf">
  <h2 class="sec">СКАЧАТЬ</h2>
  <p class="micro b" style="margin:10px 0 26px">Те же данные, свёрстанные для печати</p>
  <div class="dl">
    <a href="Расписание%2010-Л%20—%20СУНЦ%20МГУ.pdf" download>
      <b>Книга А4 · 12 полос</b>
      <span class="micro b">обложка, ключ, звонки, шесть дней, неделя, спектр</span></a>
    <a href="v1-raspisanie-10L-SUNC-MGU.pdf" download>
      <b>Плакат A3 · 10 полос</b>
      <span class="micro b">альбомный разворот, первый вариант</span></a>
    <a href="https://internat.msu.ru/structure/departments/for-students/schedule/"
       target="_blank" rel="noopener">
      <b>Источник</b>
      <span class="micro b">расписание на сайте интерната</span></a>
  </div>
</section>

<footer>
  <span class="sunc">__SUNC2__</span>
  <span class="micro">Данные: internat.msu.ru · колонка 10-Л · сверено с изображением расписания</span>
  <span class="micro">Хронохром · 2026</span>
</footer>

</div>
</main>

<script>
const D = __DATA__;
const S = 8*60+45, E = 16*60+45, SPAN = E - S;
const hh = m => String(m/60|0).padStart(2,'0')+':'+String(m%60).padStart(2,'0');
const pct = m => (m - S) / SPAN * 100;
const ink = (hex,t)=>{const n=parseInt(hex.slice(1),16),r=n>>16,g=(n>>8)&255,b=n&255,
  k=c=>Math.round(c+(10-c)*t);return `rgb(${k(r)},${k(g)},${k(b)})`;};
const skl = n => (n>1&&n<5) ? 'урока' : 'уроков';

document.getElementById('mark').innerHTML = [...'10-Л']
  .map((c,i)=>`<span style="animation-delay:${380+i*70}ms">${c}</span>`).join('');

/* ── спектр недели ── */
const spec=document.getElementById('spectrum'), caps=document.getElementById('caps');
spec.style.setProperty('--sh','clamp(180px,24vw,320px)');
let hrs='', grid='';
for(let h=9;h<=16;h++){hrs+=`<i style="top:${pct(h*60)}%">${String(h).padStart(2,'0')}</i>`;
                       grid+=`<u style="top:${pct(h*60)}%"></u>`;}
spec.insertAdjacentHTML('beforeend',`<div class="hours">${hrs}</div>`);
D.week.forEach((day,di)=>{
  const bars = day.blocks.map((b,i)=>{
    const a=D.lessons[b.l0][0], z=D.lessons[b.l1][1];
    return `<b style="top:${pct(a)}%;height:${(z-a)/SPAN*100}%;background:${D.family[b.fam].color};
            transition-delay:${di*80+i*60}ms"></b>`;}).join('');
  spec.insertAdjacentHTML('beforeend',
    `<button class="col" data-d="${di}">${grid}${bars}</button>`);
});
caps.insertAdjacentHTML('beforeend','<div></div>');
D.week.forEach(day=>{const n=day.blocks.reduce((s,b)=>s+b.l1-b.l0+1,0);
  caps.insertAdjacentHTML('beforeend',
    `<div><div class="d">${day.name}</div><div class="n">${n} ${skl(n)}</div></div>`);});

/* зажигаем спектр, когда доехали до него */
new IntersectionObserver((es,o)=>es.forEach(e=>{ if(e.isIntersecting){
  document.querySelectorAll('.col').forEach(c=>c.classList.add('lit')); o.disconnect();}}),
  {threshold:.25}).observe(spec);

/* ── день ── */
const bar=document.getElementById('bar');
bar.innerHTML = D.week.map((d,i)=>`<button data-d="${i}">${d.short}</button>`).join('')
  + '<span class="sp"></span><button id="play">▮▮ пауза</button>';
const tl=document.getElementById('tl');
tl.style.setProperty('--th','clamp(440px,54vw,660px)');
let timer=null, cur=-1, playing=true;

function renderDay(di){
  cur=di; const day=D.week[di];
  const slots=day.blocks.reduce((s,b)=>s+b.l1-b.l0+1,0), mins=slots*45;
  const m0=D.lessons[day.blocks[0].l0][0], m1=D.lessons[day.blocks.at(-1).l1][1];
  document.getElementById('dayname').textContent=day.name.toUpperCase();
  document.getElementById('dayfacts').innerHTML=
    `<b style="color:var(--amber)">${slots} ${skl(slots)}</b> &nbsp;·&nbsp; ${hh(m0)} — ${hh(m1)}`+
    ` &nbsp;·&nbsp; ${mins/60|0} ч ${String(mins%60).padStart(2,'0')} мин`;
  document.querySelectorAll('.col').forEach(c=>c.classList.toggle('on',+c.dataset.d===di));
  document.querySelectorAll('#bar button[data-d]').forEach(b=>b.classList.toggle('on',+b.dataset.d===di));
  let h='';
  for(let x=9;x<=16;x++) h+=`<div class="hr" style="top:${pct(x*60)}%"><i>${String(x).padStart(2,'0')}</i></div>`;
  D.intervals.filter(v=>v.kind==='meal').forEach(v=>{
    const a=Math.max(v.a,S), b=Math.min(v.b,E); if(b-a<10) return;
    h+=`<div class="meal" style="top:${pct(a)}%;height:${(b-a)/SPAN*100}%">
        <span>${v.name.toUpperCase()}</span></div>`;});
  const busy=new Set();
  day.blocks.forEach((b,i)=>{
    for(let n=b.l0;n<=b.l1;n++) busy.add(n);
    const col=D.family[b.fam].color, a=D.lessons[b.l0][0], z=D.lessons[b.l1][1];
    const ic=ink(col,.88), i2=ink(col,.55), i3=ink(col,.72);
    let meta='';
    for(let n=b.l0;n<=b.l1;n++){const [la,lb]=D.lessons[n];
      meta+=`<u style="top:${(la-a)/(z-a)*100}%;height:${(lb-la)/(z-a)*100}%;
             background:${ink(col,.15)}"><em style="color:${i2}">${n}</em>
             <s style="color:${i3}">${hh(la)}\n${hh(lb)}</s></u>`;}
    h+=`<div class="blk" style="top:${pct(a)}%;height:${(z-a)/SPAN*100}%;background:${col};
         animation-delay:${i*80}ms"><div class="meta">${meta}</div><div class="body">
         <div style="display:flex;align-items:baseline;min-width:0">
           <span class="nm" style="color:${ic}">${b.name}</span>
           ${b.note?`<span class="note" style="color:${i2}">${b.note}</span>`:''}</div>
         <div class="rt">${b.room?`<div class="room" style="color:${ic}"><i>каб.</i>${b.room}</div>`:''}
           ${b.teacher?`<div class="tch" style="color:${ic}">${b.teacher}</div>`:''}</div></div></div>`;});
  for(let n=1;n<=8;n++){ if(busy.has(n)) continue; const [a,b]=D.lessons[n];
    h+=`<div class="free" style="top:${pct(a)}%;height:${(b-a)/SPAN*100}%">
        <em>${n}</em><s>свободно</s></div>`;}
  const now=new Date(), wd=now.getDay();
  if(wd>=1&&wd<=6&&wd-1===di){const m=now.getHours()*60+now.getMinutes();
    if(m>=S&&m<=E) h+=`<div class="now" style="top:${pct(m)}%"><b>сейчас ${hh(m)}</b></div>`;}
  tl.innerHTML=h;
}
function tick(){clearInterval(timer); if(playing) timer=setInterval(()=>renderDay((cur+1)%6),4600);}
function go(d){renderDay(d);tick();}
document.querySelectorAll('.col').forEach(c=>c.onclick=()=>{playing=false;setPlay();go(+c.dataset.d);
  document.getElementById('den').scrollIntoView({block:'start'});});
document.querySelectorAll('#bar button[data-d]').forEach(b=>b.onclick=()=>{playing=false;setPlay();go(+b.dataset.d);});
const pb=document.getElementById('play');
function setPlay(){pb.textContent=playing?'▮▮ пауза':'▶ листать';pb.classList.toggle('on',playing);tick();}
pb.onclick=()=>{playing=!playing;setPlay();};

/* ── звонки ── */
const rows=Object.entries(D.lessons).map(([n,[a,b]])=>({les:1,n,nm:'урок',a,b}))
  .concat(D.intervals.map(v=>({les:0,n:'',nm:v.name,a:v.a,b:v.b,meal:v.kind==='meal'})))
  .sort((x,y)=>x.a-y.a);
document.getElementById('bells').innerHTML=rows.map(r=>`
  <div class="brow ${r.les?'les':(r.meal?'eat':'')}">
    <span class="no">${r.n}</span><span class="nm">${r.nm}</span>
    <span class="t">${hh(r.a)}</span><span>—</span><span class="t">${hh(r.b)}</span>
    <span class="du">${r.b-r.a} мин</span></div>`).join('');

/* ── предметы ── */
const tally={};
D.week.forEach(d=>d.blocks.forEach(b=>tally[b.fam]=(tally[b.fam]||0)+b.l1-b.l0+1));
const ord=Object.entries(tally).sort((a,b)=>b[1]-a[1]||D.family[a[0]].title.localeCompare(D.family[b[0]].title));
const maxN=ord[0][1];
document.getElementById('subj').innerHTML=ord.map(([f,n])=>`
  <div class="srow"><i style="background:${D.family[f].color}"></i>
    <span class="t">${D.family[f].title}</span><span class="n" style="color:${D.family[f].color}">${n}</span>
    <span class="h">${n*45/60|0}:${String(n*45%60).padStart(2,'0')}</span>
    <span class="track"><b data-w="${n/maxN*100}" style="background:${D.family[f].color}"></b></span>
  </div>`).join('');
new IntersectionObserver((es,o)=>es.forEach(e=>{if(e.isIntersecting){
  document.querySelectorAll('.srow .track b').forEach((b,i)=>
    setTimeout(()=>b.style.width=b.dataset.w+'%', i*70)); o.disconnect();}}),
  {threshold:.2}).observe(document.getElementById('subj'));

const wd=new Date().getDay();
go(wd>=1&&wd<=6?wd-1:0); setPlay();
</script></body></html>
"""

MESH = ('<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">'
        '<defs><pattern id="hex" width="72" height="124.7" patternUnits="userSpaceOnUse">'
        '<path d="M36 0 L72 20.8 L72 62.35 L36 83.1 L0 62.35 L0 20.8 Z" fill="none" '
        'stroke="#1E2635" stroke-width="1"/>'
        '<path d="M36 83.1 L36 124.7" fill="none" stroke="#1E2635" stroke-width="1"/>'
        '</pattern></defs><rect width="100%" height="100%" fill="url(#hex)"/></svg>')

html = (HTML.replace('__DATA__', json.dumps(payload, ensure_ascii=False))
            .replace('__MESH__', MESH)
            .replace('__SUNC__', svg_sunc(30))
            .replace('__SUNC2__', svg_sunc(34))
            .replace('__RING__', svg_ring(60)))
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)
print('ОК →', OUT, os.path.getsize(OUT), 'байт')
