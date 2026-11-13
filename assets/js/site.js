/* The portfolio console is a local, read-only interface; it never executes OS commands. */
(() => {
  'use strict';
  const SETTINGS = Object.freeze({
    brandGithub: 'https://github.com/Melo-Technology',
    personalGithub: 'https://github.com/Danieljucke',
    brandTwitter: '', // Add the official Mélo Technology X/Twitter URL after verification.
    email: 'melotechnology@proton.me',
    portfolio: 'https://danieljucke.github.io/Portfolio/'
  });
  const STACK = Object.freeze({
    frontend: ['Flutter / Dart', 'React', 'Vue.js', 'TypeScript', 'JavaScript', 'HTML / CSS'],
    backend: ['Python', 'FastAPI', 'Node.js / Express', 'C# / .NET 8', 'REST APIs'],
    data: ['SQLite', 'PostgreSQL', 'MySQL', 'MongoDB', 'SQL / Prisma'],
    tooling: ['Docker', 'Git', 'GitHub Actions', 'pytest', 'Flutter tests', 'CI/CD']
  });
  const PROJECTS = Object.freeze({
    netshare: 'NetShare — desktop server and cross-platform player for accessing personal media. Site: https://netshareplayer.com',
    meloshelf: 'MeloShelf — Python-based, local-first Windows music library organizer. https://github.com/Danieljucke/MeloShelf',
    antmap: 'AntMap — cross-platform social application under active development. Public demo not verified.',
    ecg: 'ECG Research — experimental ECG image/signal analysis and model validation; not a medical diagnostic tool.',
    'dream-teller': 'Dream-Teller — creative project in development. Public description and demo pending verification.',
    clustriva: 'Clustriva — local file and folder workflow tools with a Python core and web interface. Coming soon.',
    'media-filter': 'Media Duplicate Finder — visual duplicate review for images and videos. https://github.com/Danieljucke/Media-filter',
    'deezer-to-spotify': 'Deezer to Spotify — playlist transfer utility. https://github.com/Danieljucke/DeezerToSpotify',
    spotifilter: 'SpotiFilter — Spotify playlist organization utility. https://github.com/Danieljucke/SpotiFilter'
  });
  const root = document.documentElement;
  const safeStorage = {
    get(key) { try { return localStorage.getItem(key); } catch { return null; } },
    set(key, value) { try { localStorage.setItem(key, value); } catch { /* Optional preference. */ } }
  };
  const requestedTheme = safeStorage.get('melo-portfolio-theme');
  const preferredDark = window.matchMedia?.('(prefers-color-scheme: dark)').matches ?? true;
  root.dataset.theme = ['dark','light'].includes(requestedTheme) ? requestedTheme : preferredDark ? 'dark' : 'light';
  root.dataset.accent = ['blue','copper','teal'].includes(safeStorage.get('melo-portfolio-accent')) ? safeStorage.get('melo-portfolio-accent') : 'blue';
  function setTheme(value) {
    const next = value === 'toggle' ? (root.dataset.theme === 'dark' ? 'light' : 'dark') : value;
    if (!['dark','light'].includes(next)) return false;
    root.dataset.theme = next;
    safeStorage.set('melo-portfolio-theme', next);
    document.querySelectorAll('[data-theme-toggle]').forEach(button => {
      button.textContent = next === 'dark' ? 'Light mode' : 'Dark mode';
      button.setAttribute('aria-label', next === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    });
    return true;
  }
  function setAccent(value) {
    if (!['blue','copper','teal'].includes(value)) return false;
    root.dataset.accent = value;
    safeStorage.set('melo-portfolio-accent', value);
    return true;
  }
  document.querySelectorAll('[data-theme-toggle]').forEach(button => button.addEventListener('click', () => setTheme('toggle')));
  setTheme(root.dataset.theme);

  document.querySelectorAll('[data-brand-social="github"]').forEach(link => {
    link.href = SETTINGS.brandGithub;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
  });
  document.querySelectorAll('[data-brand-social="twitter"]').forEach(node => {
    if (!SETTINGS.brandTwitter) {
      node.textContent = 'X / Twitter · handle pending';
      node.setAttribute('title', 'Official brand handle has not been confirmed');
    } else {
      const link = document.createElement('a');
      link.href = SETTINGS.brandTwitter;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = 'X / Twitter';
      node.replaceWith(link);
    }
  });

  const signalCanvas = document.querySelector('[data-signal-canvas]');
  if (signalCanvas?.getContext) {
    const frame = signalCanvas.parentElement;
    const ctx = signalCanvas.getContext('2d');
    const reduceMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;
    let width = 0, height = 0, tick = 0, pulses = 0, rafId = 0, visible = true;
    const count = document.querySelector('[data-signal-count]');
    const strands = Array.from({length: 13}, (_, i) => (i - 6) * 12);
    const resize = () => {
      const scale = Math.min(window.devicePixelRatio || 1, 2);
      width = frame.clientWidth; height = frame.clientHeight;
      signalCanvas.width = Math.max(1, Math.round(width * scale));
      signalCanvas.height = Math.max(1, Math.round(height * scale));
      ctx.setTransform(scale,0,0,scale,0,0);
      draw();
    };
    function draw() {
      if (!width || !height) return;
      ctx.clearRect(0,0,width,height);
      const css = getComputedStyle(root);
      const blue = css.getPropertyValue('--blue').trim();
      const copper = css.getPropertyValue('--copper').trim();
      strands.forEach((offset,index) => {
        const from = height*.7 + offset * .6;
        const target = height*.5 + offset*.12;
        ctx.beginPath();
        ctx.moveTo(-45,from);
        ctx.bezierCurveTo(width*.34,from - 65 - Math.sin(tick*.012+index)*13,width*.58,target+82,width*.93,target);
        ctx.strokeStyle = index % 4 === 0 ? copper : blue;
        ctx.globalAlpha = (index%4 === 0 ? .42 : .22) + (pulses>0?.10:0);
        ctx.lineWidth = index%4===0?1.3:.8;
        ctx.stroke();
        if(index%2===0){
          const t = ((tick*.00055+index*.12)%1);
          const x = width*(t*.95), y=from+(target-from)*t-Math.sin(Math.PI*t)*30;
          ctx.fillStyle = index%4===0?copper:blue;ctx.globalAlpha=.6;
          ctx.beginPath();ctx.arc(x,y,2+(pulses>0?.8:0),0,Math.PI*2);ctx.fill();
        }
      });
      ctx.globalAlpha=1;
      if(pulses>0) pulses--;
    }
    let last=0;
    function animate(ms){if(!visible)return;if(ms-last>32){tick++;draw();last=ms}rafId=requestAnimationFrame(animate)}
    const observer=new IntersectionObserver(entries => {
      visible=entries[0].isIntersecting;
      cancelAnimationFrame(rafId);
      if(visible&&!reduceMotion)rafId=requestAnimationFrame(animate);
      else if(visible)draw();
    });
    observer.observe(frame);
    document.querySelector('[data-signal-trigger]')?.addEventListener('click',()=>{
      pulses=55;
      if(count)count.textContent=String(Number(count.textContent||'0')+1);
      draw();
    });
    window.addEventListener('resize',resize,{passive:true});
    resize();
    new MutationObserver(draw).observe(root,{attributes:true,attributeFilter:['data-theme','data-accent']});
  }

  const input = document.querySelector('[data-console-input]');
  const output = document.querySelector('[data-console-output]');
  const form = document.querySelector('[data-console-form]');
  if(input && output && form){
    const commands = ['help','whoami','about','projects','project','stack','links','github','twitter','contact','status','ping','theme','accent','date','uptime','history','clear','echo','ls','cat','go','coffee'];
    const history=[];
    let cursor=0;
    const started=Date.now();
    function line(text,type='normal'){
      const p=document.createElement('p');
      if(type!=='normal')p.className=type;
      p.textContent=text;
      output.appendChild(p);
      while(output.childElementCount>120)output.firstElementChild.remove();
      output.scrollTop=output.scrollHeight;
      return p;
    }
    function anchor(label,url){
      const p=line('');const a=document.createElement('a');
      a.textContent=label;a.href=url;a.target='_blank';a.rel='noopener noreferrer';p.appendChild(a);
      output.scrollTop=output.scrollHeight;
    }
    const allProjects=Object.keys(PROJECTS);
    const handlers={
      help(){line('Commands: help, whoami, projects, project <name>, stack [group], links, github, twitter, contact, status, ping <server|player>, theme <dark|light|toggle>, accent <blue|copper|teal>, date, uptime, history, clear, echo <text>, go <section>','ok');line('Tip: Up/Down for command history; Tab completes commands. This is a safe portfolio demo, not a real system shell.');},
      whoami(){line('Daniel Joy · Software Engineer · Mélo Technology');},
      about(){line('Cross-platform apps, reliable local-first tools, security-conscious engineering and experimental research.');},
      projects(){line(allProjects.join('  ·  '));},
      project(args){const key=args.join('-').toLowerCase();if(PROJECTS[key])line(PROJECTS[key]);else line('Unknown project. Try: projects','error');},
      stack(args){const key=args[0]?.toLowerCase();if(!key){Object.entries(STACK).forEach(([group,items])=>line(group.padEnd(10)+' '+items.join(' · ')));return;}if(STACK[key])line(key+': '+STACK[key].join(' · '));else line('Unknown stack group. Choose frontend, backend, data or tooling.','error');},
      links(){anchor('Mélo Technology · GitHub',SETTINGS.brandGithub);anchor('Danieljucke · GitHub',SETTINGS.personalGithub);anchor('NetShare website','https://netshareplayer.com');if(SETTINGS.brandTwitter)anchor('Mélo Technology · X',SETTINGS.brandTwitter);else line('Mélo Technology X / Twitter: official handle not configured.','error');},
      github(){anchor('Mélo Technology source repositories',SETTINGS.brandGithub);},
      twitter(){if(SETTINGS.brandTwitter)anchor('Mélo Technology on X',SETTINGS.brandTwitter);else line('Official X / Twitter handle pending verification.','error');},
      contact(){anchor('Send an email','mailto:'+SETTINGS.email);},
      status(){line('Portfolio: static / local interactions only. Network health: not measured. Clustriva: coming soon.','ok');},
      ping(args){const target=(args[0]||'').toLowerCase();if(!['server','player'].includes(target)){line('Usage: ping server | ping player','error');return;}line('Simulated signal dispatched to '+target+'. This is an animation demo; no network request was sent.','ok');document.querySelector('[data-signal-trigger]')?.click();},
      theme(args){if(setTheme(args[0]||'toggle'))line('Theme: '+root.dataset.theme,'ok');else line('Usage: theme dark | light | toggle','error');},
      accent(args){if(setAccent(args[0]||''))line('Accent: '+root.dataset.accent,'ok');else line('Usage: accent blue | copper | teal','error');},
      date(){line(new Date().toLocaleString('en-GB',{dateStyle:'full',timeStyle:'long'}));},
      uptime(){const n=Math.floor((Date.now()-started)/1000);line('Session uptime: '+Math.floor(n/60)+'m '+(n%60)+'s');},
      history(){line(history.map((s,i)=>String(i+1).padStart(2,' ')+'  '+s).join('\n')||'No commands yet.');},
      clear(){output.replaceChildren();},
      echo(args){line(args.join(' '));},
      ls(){line('netshare/  meloshelf/  antmap/  ecg-research/  dream-teller/  clustriva/  fullstack/');},
      cat(args){if(args.join(' ')==='README.md')line('Build useful tools. Make limitations explicit. Keep the code understandable.');else line('Only README.md is available in this demonstration.','error');},
      go(args){const map={home:'top',work:'work',projects:'work',stack:'capabilities',console:'console',contact:'contact'};const target=map[args[0]];const el=target&&document.getElementById(target);if(!el){line('Usage: go home | work | stack | console | contact','error');return;}el.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});line('Navigating to '+args[0]+'.','ok');},
      coffee(){line('HTTP 418 · Keeping the compiler caffeinated.','ok');}
    };
    function execute(value){
      const raw=value.trim();if(!raw)return;
      line('visitor@portfolio:~$ '+raw,'prompt');
      history.push(raw);if(history.length>50)history.shift();cursor=history.length;
      const words=raw.match(/(?:[^\s"]+|"[^"]*")+/g)||[];
      const command=words.shift()?.toLowerCase();
      const args=words.map(x=>x.replace(/^"|"$/g,''));
      if(Object.prototype.hasOwnProperty.call(handlers,command))handlers[command](args);
      else line('Unknown command: '+command+'. Type help.','error');
    }
    form.addEventListener('submit',event=>{event.preventDefault();const value=input.value;input.value='';execute(value);input.focus();});
    input.addEventListener('keydown',event=>{
      if(event.key==='ArrowUp'){event.preventDefault();cursor=Math.max(0,cursor-1);input.value=history[cursor]||'';}
      else if(event.key==='ArrowDown'){event.preventDefault();cursor=Math.min(history.length,cursor+1);input.value=history[cursor]||'';}
      else if(event.key==='Tab'){
        const prefix=input.value.trim().toLowerCase();if(prefix.includes(' '))return;
        const matches=commands.filter(c=>c.startsWith(prefix));
        if(matches.length===1){event.preventDefault();input.value=matches[0]+' ';}
        else if(matches.length>1&&prefix){event.preventDefault();line(matches.join('  '));}
      }
    });
    document.querySelectorAll('[data-command]').forEach(button=>button.addEventListener('click',()=>execute(button.dataset.command)));
    line('Mélo Technology · Portfolio terminal v1','ok');
    line('Type help to explore projects, stack, links and appearance. No real shell access.');
  }
})();
