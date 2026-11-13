from playwright.sync_api import sync_playwright
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from functools import partial
import json
root=Path(__file__).resolve().parents[1]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root)))
Thread(target=server.serve_forever,daemon=True).start()
origin=f'http://127.0.0.1:{server.server_port}'
logs=[]
evidence=root/'docs'/'validation'/'product-v2'
evidence.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for width,height in [(360,800),(390,844),(768,1024),(1024,800),(1440,900)]:
  for mode in ['dark','light']:
   page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1,reduced_motion='reduce')
   errors=[]
   page.on('pageerror',lambda err:errors.append(str(err)))
   page.on('console',lambda msg:errors.append(msg.text) if msg.type=='error' else None)
   page.goto(origin+'/index.html',wait_until='domcontentloaded',timeout=20000)
   page.evaluate('mode=>document.documentElement.dataset.theme=mode',mode)
   page.wait_for_timeout(60)
   overflow=page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 2')
   overflowElements=page.evaluate('''() => [...document.querySelectorAll('body *')].filter(x=>{let r=x.getBoundingClientRect();return r.right>window.innerWidth+4}).slice(0,5).map(x=>({tag:x.tagName,cls:x.className?.toString().slice(0,60),right:x.getBoundingClientRect().right}))''') if overflow else []
   logs.append({'viewport':width,'mode':mode,'overflow':overflow,'elements':overflowElements,'errors':errors})
   if width==1440 and mode=='dark': page.screenshot(path=str(evidence/'after-desktop-dark.png'),full_page=True,animations='disabled',timeout=20000)
   if width==1440 and mode=='light': page.screenshot(path=str(evidence/'after-desktop-light.png'),full_page=True,animations='disabled',timeout=20000)
   if width==390 and mode=='dark': page.screenshot(path=str(evidence/'after-mobile-dark.png'),full_page=True,animations='disabled',timeout=20000)
   page.close()
 for fname in ['server.html','player.html','fullstack.html']:
  page=browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce');errors=[]
  page.on('pageerror',lambda err:errors.append(str(err)))
  page.on('console',lambda msg:errors.append(msg.text) if msg.type=='error' else None)
  page.goto(origin+'/'+fname,wait_until='domcontentloaded',timeout=20000)
  logs.append({'page':fname,'overflow':page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),'errors':errors})
  page.close()
 page=browser.new_page(viewport={'width':1280,'height':900},reduced_motion='reduce')
 page.goto(origin+'/index.html',wait_until='domcontentloaded',timeout=20000)
 inp=page.locator('[data-console-input]');
 def send(s): inp.fill(s);inp.press('Enter')
 send('help');send('stack');send('stack backend');send('projects');send('project clustriva');send('twitter');send('ping server');send('theme light');send('accent copper')
 out=page.locator('[data-console-output]').inner_text()
 assert 'Node.js / Express' in out
 assert 'dream-teller' in out
 assert 'Coming soon' in out
 assert 'handle pending verification' in out
 assert 'no network request was sent' in out
 assert page.locator('html').get_attribute('data-theme')=='light'
 assert page.locator('html').get_attribute('data-accent')=='copper'
 send('theme dark');assert page.locator('html').get_attribute('data-theme')=='dark'
 inp.fill('who');inp.press('Tab');assert inp.input_value().startswith('whoami')
 inp.press('Enter');inp.press('ArrowUp');assert inp.input_value().strip()=='whoami'
 send('clear');assert page.locator('[data-console-output]').inner_text().strip()==''
 assert page.locator('[data-signal-count]').inner_text()=='1'
 link=page.locator('[data-brand-social="github"]').first
 assert link.get_attribute('href')=='https://github.com/Melo-Technology'
 assert page.locator('[data-brand-social="twitter"]').first.evaluate('(el)=>el.tagName')=='SPAN'
 links=page.locator('a[href^="#"]')
 anchors=[(links.nth(i).get_attribute('href'),page.locator(links.nth(i).get_attribute('href')).count()) for i in range(links.count())]
 assert all(n for _,n in anchors),anchors
 commands=['help','whoami','about','projects','project meloshelf','stack','stack frontend','stack backend','stack data','stack tooling','links','github','twitter','contact','status','ping player','theme light','accent teal','date','uptime','history','echo safe text','ls','cat README.md','go work','coffee']
 for command in commands:
  send('clear');send(command)
  assert 'Unknown command:' not in page.locator('[data-console-output]').inner_text(),command
 send('<img src=x onerror=alert(1)>')
 assert page.locator('[data-console-output] img').count()==0
 assert page.locator('[data-console-output]').inner_text().find('<img src=x onerror=alert(1)>')>=0
 page.reload(wait_until='domcontentloaded')
 page.keyboard.press('Tab')
 assert page.evaluate('document.activeElement.classList.contains("skip-link")')
 assert page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches")
 logs.append({'console_tests':'pass','internal_anchors':anchors})
 page.close();browser.close()
server.shutdown()
Path(evidence/'browser-results.json').write_text(json.dumps(logs,indent=2),encoding='utf-8')
print(json.dumps(logs,indent=2))
if any(x.get('overflow') or x.get('errors') for x in logs):raise SystemExit('Failed browser checks')
