from pathlib import Path
import os, shutil, socket, subprocess, time, urllib.request, webbrowser, zipfile, secrets
from getpass import getpass
PORT=3004
URL=f'http://localhost:{PORT}'
root=Path.home()/'VibeGuard-V7'
project=root/'vibeguard-member4'
npm=shutil.which('npm.cmd') or shutil.which('npm')
if not npm or not shutil.which('node'): raise RuntimeError('Install Node.js LTS first.')
for host,family in [('127.0.0.1',socket.AF_INET),('::1',socket.AF_INET6)]:
    with socket.socket(family,socket.SOCK_STREAM) as s:
        s.settimeout(1)
        if s.connect_ex((host,PORT))==0: raise RuntimeError('Port 3004 is occupied. Stop your previous VibeGuard server first.')
if not (project/'package.json').exists():
    name='vibeguard-member4-v7.zip'
    locations=[Path.cwd()/name,Path.home()/'Downloads'/name,Path.home()/'Desktop'/name]
    if '__file__' in globals(): locations.insert(0,Path(__file__).resolve().parent/name)
    archive=next((p for p in locations if p.is_file()),None)
    if archive is None: raise FileNotFoundError('Download '+name+' first.')
    root.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        for item in z.infolist():
            if not (root/item.filename).resolve().is_relative_to(root.resolve()): raise RuntimeError('Unsafe archive path')
        z.extractall(root)
env=project/'.env.local'
if not env.exists():
    old=next((p for v in [6,5,4,3,2] if (p:=Path.home()/f'VibeGuard-V{v}'/'vibeguard-member4'/'.env.local').exists()),None)
    shutil.copyfile(old or project/'.env.example',env)
lines=env.read_text(encoding='utf-8').splitlines()
def set_value(key,value):
    global lines
    lines=[l for l in lines if l.split('=',1)[0].strip()!=key]
    lines.append(f'{key}={value}')
def value(key):
    return next((l.split('=',1)[1].strip().strip('"\'') for l in reversed(lines) if '=' in l and l.split('=',1)[0].strip()==key),'')
for key in ['NEXTAUTH_URL_INTERNAL','AUTH_URL']:
    lines=[l for l in lines if l.split('=',1)[0].strip()!=key]
set_value('NEXTAUTH_URL',URL)
if not value('GOOGLE_CLIENT_ID'): set_value('GOOGLE_CLIENT_ID',input('Google Client ID: ').strip())
if not value('GOOGLE_CLIENT_SECRET'): set_value('GOOGLE_CLIENT_SECRET',getpass('Google Client Secret: ').strip())
if not value('NEXTAUTH_SECRET'): set_value('NEXTAUTH_SECRET',secrets.token_urlsafe(48))
env.write_text('\n'.join(lines)+'\n',encoding='utf-8')
runtime=os.environ.copy()
for key in ['NEXTAUTH_URL_INTERNAL','AUTH_URL','GOOGLE_CLIENT_ID','GOOGLE_CLIENT_SECRET','NEXTAUTH_SECRET','NEXT_PUBLIC_API_URL']: runtime.pop(key,None)
runtime['NEXTAUTH_URL']=URL
print('Installing dependencies...')
subprocess.run([npm,'install'],cwd=project,env=runtime,check=True)
print('Building VibeGuard 7.0...')
subprocess.run([npm,'run','build'],cwd=project,env=runtime,check=True)
log=project/'server.log'
with log.open('w',encoding='utf-8') as f:
    server=subprocess.Popen([npm,'run','start','--','-p',str(PORT)],cwd=project,env=runtime,stdout=f,stderr=subprocess.STDOUT)
for _ in range(60):
    if server.poll() is not None: break
    try:
        with urllib.request.urlopen(URL,timeout=2) as r:
            if r.status==200:
                webbrowser.open(URL); print('Ready:',URL); print('Google callback:',URL+'/api/auth/callback/google'); break
    except OSError: pass
    time.sleep(2)
else:
    print(log.read_text(encoding='utf-8',errors='replace')[-4000:]); raise RuntimeError('Server did not start')
if server.poll() is not None: raise RuntimeError('Server exited; inspect '+str(log))
