from flask import Flask, render_template, url_for, redirect, request
from api import system, spider, person
app = Flask(__name__)


@app.route('/')
@app.route('/contest')
def index():
    _system = system.system()
    _contests = _system.getContestList()
    return render_template('index.html',
                            p1='active',
                            contests = _contests
                            )

@app.route('/setup/position')
def getPosition():
    _system = system.system()
    _positions = _system.getPositionMsg()
    # print(_positions)
    return render_template('position.html',
                            p2='active',
                            positions = _positions
                            )

@app.route('/setup/position', methods=['POST'])
def setPosition():
    _system = system.system()
    _system.setPositionMsg(request.form)
    return redirect('/setup/position')

@app.route('/setup/balloon')
def getBalloon():
    _system = system.system()
    _balloon = _system.getBalloonMsg()
    return render_template('balloon.html',
                            p3='active',
                            balloons = _balloon)

@app.route('/setup/balloon', methods=['POST'])
def setBalloon():
    _system = system.system()
    _system.setBalloonMsg(request.form)
    return redirect('/setup/balloon')

@app.route('/contest/<id>')
def contest(id):
    id = int(id)
    _system = system.system(id)
    _msglist = _system.getMsg()
    _contestname = _system.getContestName(id)
    return render_template('contest.html',
                            p1='active',
                            contestid = id,
                            contestname = _contestname,
                            msglist=_msglist)

@app.route('/contest/<id>', methods=["POST"])
def refresh(id):
    id = int(id)
    _system = system.system(id)
    # print(dict(request.form))
    _system.handleMsg(dict(request.form))
    return redirect('/contest/'+str(id))

@app.route('/addcontest', methods=['POST'])
def addcontest():
    _system = system.system()
    _system.addContest(request.form['cname'], request.form['cid'])
    return redirect('/contest')

@app.route('/delcontest/<id>')
def delcontest(id):
    id = int(id)
    _system = system.system()
    _system.delContest(id)
    return redirect('/contest')

@app.route('/clear')
def clear():
    _system = system.system()
    _system.clearData()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)