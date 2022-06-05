import os
from flask import Flask, redirect, request, url_for
from pwnboxlib.interpreter.duckyscriptinterpreter import DuckyScriptInterpeter

app = Flask(__name__)

def nextnonexistent(f):
    fnew = f
    root, ext = os.path.splitext(f)
    i = 0
    while os.path.exists(fnew):
        i += 1
        fnew = '%s_%i%s' % (root, i, ext)
    return fnew


script_links = {}
script_count = 1

print(f'{os.path.abspath(os.path.dirname(__file__))}/usbrubberducky-payloads/payloads/library/')
for dir, sdir, file in os.walk(f'{os.path.abspath(os.path.dirname(__file__))}/usbrubberducky-payloads/payloads/library/'):
    if 'payload.txt' in file:
        fullpath = dir + '/' + 'payload.txt'
        script_links[f'{script_count}:  {os.path.basename(dir)}'] = fullpath
        script_count += 1


@app.route('/extract', methods = ['POST'])
def extract():
    os.system('mkdir -p ./extractions/')
    with open(nextnonexistent('extractions/extraction.txt'), 'w') as f:
        for param in request.form:
            f.write(param)
    return redirect('/')


@app.route('/exec', methods = ['POST'])
def run_script():
    if request.form['script']:
        script_link = str(request.form['script'])
        if script_link in script_links:
            DuckyScriptInterpeter.exec_script(os.path.abspath(script_links[script_link]))
    return redirect('/')


@app.route('/')
def scripts():
    html = '<ul>'
    for link in dict(script_links).keys():
        html += f'<li><form action="/exec" method="post"><input type="submit" value="{link}" name="script" /></form></li>'
    html += '</ul>'
    return html


def main():
    app.run('0.0.0.0', 5000)
    pass


if __name__ == '__main__':
    main()