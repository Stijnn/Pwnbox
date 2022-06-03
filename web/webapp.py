import os
from flask import Flask, redirect, request, url_for
from pwnboxlib.interpreter.duckyscriptinterpreter import DuckyScriptInterpeter

app = Flask(__name__)


script_links = {}
script_count = 1
for dir, sdir, file in os.walk('../scripts/usbrubberducky-payloads/payloads/library/'):
    if 'payload.txt' in file:
        fullpath = dir + '/' + 'payload.txt'
        script_links[f'{script_count}:  {os.path.basename(dir)}'] = fullpath
        script_count += 1



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
    app.run()
    pass


if __name__ == '__main__':
    main()