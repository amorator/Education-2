from os import path, chdir
from flask import url_for, request, Response, jsonify, make_response
from json import dumps
from classes.worker import Worker
from classes.project import Project
from modules.server import Server

chdir(path.dirname(path.realpath(__file__)))

app = Server()

@app.errorhandler(404)
def page_not_found(error):
    return 'Ошибка.\nУказанный маршрут не найден.', 404

@app.errorhandler(405)
def method_not_allowed(error):
    return 'Ошибка.\nМетод не зоответствует запросу.', 405


@app.route('/', methods=['GET'])
def index():
    return 'Сервер исправен и готов к работе!', 200


@app.route('/projects', methods=['GET'])
def project():
    p = app.sql.project_all()
    if p:
        return dumps(p, indent=4, ensure_ascii=False), 200
    return None, 200

@app.route('/projects/<int:id>', methods=['GET'])
def project_id(id):
    p = app.sql.project_by_id(id, json=True)
    if p:
        return dumps(p, indent=4, ensure_ascii=False), 200
    return 'Ошибка!\nУказанная запись не найдена.', 400

@app.route('/projects/stats', methods=['GET'])
def project_stats():
    projects = app.sql.project_all(json=False)
    if not projects:
        return {'projects': projects}, 200
    s = 0
    f = 0
    p = 0
    for i in projects:
        x = i.stat()
        if x == 1:
            s += 1
        elif x == -1:
            f += 1
        else:
            p += 1
    return {'projects': {'successed': s, 'failed': f, 'in_progess': p}}, 200

@app.route('/projects/add/<string:name>/<int:wid>/<string:desc>/<int:stage>', methods=['POST'])
@app.route('/projects/add/<string:name>/<int:wid>/<string:desc>', methods=['POST'])
@app.route('/projects/add/<string:name>/<int:wid>', methods=['POST'])
def project_add(name, wid, desc='', stage=1):
    if app.sql.project_add(Project(0, name, wid, desc, stage)):
        return 'Проект добавлен!', 201
    return 'Ошибка!\nПроверьте запрос.', 400

@app.route('/projects/update/<int:id>/<string:name>/<int:wid>/<string:desc>/<int:stage>', methods=['PUT'])
@app.route('/projects/update/<int:id>/<string:name>/<int:wid>/<string:desc>', methods=['PUT'])
@app.route('/projects/update/<int:id>/<string:name>/<int:wid>', methods=['PUT'])
@app.route('/projects/update/<int:id>/<string:name>', methods=['PUT'])
def project_update(id, name=' ', wid=0, desc=' ', stage=-1):
    p0 = Project(id, name, wid, desc, stage)
    p = app.sql.project_by_id(id)
    if not p:
        return 'Ошибка!\nУказанная запись не найдена.', 400
    if p.merge(p0) and app.sql.project_update(p):
        return 'Проект обновлен!', 205
    return 'Ошибка!\nПроверьте запрос.', 400

@app.route('/projects/delete/<int:id>', methods=['POST'])
def project_delete(id):
    if app.sql.project_by_id(id) and app.sql.project_delete(id):
        return 'Проект удален!', 205
    return 'Ошибка!\nПроверьте запрос.', 400

@app.route('/projects/next_stage/<int:id>', methods=['PUT'])
def project_next_stage(id):
    p = app.sql.project_by_id(id)
    if not p:
        return 'Ошибка!\nУказанная запись не найдена.', 400
    if not p.next_stage():
        return 'Ошибка!\nУказанный проект невозможно перевести на следющую стадию.', 400
    if app.sql.project_update(p):
        return 'Проект переведен на следующую стадию!', 205
    return 'Ошибка!\nПроверьте запрос.', 400

@app.route('/projects/fail/<int:id>', methods=['PUT'])
def project_fail(id):
    p = app.sql.project_by_id(id)
    if not p:
        return 'Ошибка!\nУказанная запись не найдена.', 400
    if not p.fail():
        return 'Ошибка!\nУказанный проект закрыт.', 400
    if app.sql.project_update(p):
        return 'Проект отмечен как проваленный!', 205
    return 'Ошибка!\nПроверьте запрос.', 400


@app.route('/workers', methods=['GET'])
def worker():
    p = app.sql.worker_all()
    if p:
        return dumps(p, indent=4, ensure_ascii=False), 200
    return None, 200

@app.route('/workers/stats', methods=['GET'])
def worker_stats():
    workers = app.sql.worker_all(json=False)
    if not workers:
        return {'workers': workers}, 200
    res = {'workers': {}}
    for w in workers:
        res['workers'][w.id] = {'successed': 0, 'failed': 0, 'in_progress': 0}
        projects = app.sql.project_by_wid(w.id)
        if projects:
            for p in projects:
                x = p.stat()
                if x == 1:
                    res['workers'][w.id]['successed'] += 1
                elif x == -1:
                    res['workers'][w.id]['failed'] += 1
                else:
                    res['workers'][w.id]['in_progress'] += 1
    return res, 200

@app.route('/workers/<int:id>', methods=['GET'])
def worker_id(id):
    p = app.sql.worker_by_id(id, json=True)
    if p:
        return dumps(p, indent=4, ensure_ascii=False), 200
    return 'Ошибка!\nУказанная запись не найдена.', 400

@app.route('/workers/add/<string:name>/<string:speciality>/<string:experience>', methods=['POST'])
@app.route('/workers/add/<string:name>/<string:speciality>', methods=['POST'])
def worker_add(name, speciality, experience=''):
    if Worker.is_exp(experience) and app.sql.worker_add(Worker(0, name, speciality, experience)):
        return 'Работник добавлен!', 201
    return 'Ошибка!\nПроверьте запрос.', 400

@app.route('/workers/update/<int:id>/<string:name>/<string:speciality>/<string:experience>', methods=['PUT'])
@app.route('/workers/update/<int:id>/<string:name>/<string:speciality>', methods=['PUT'])
@app.route('/workers/update/<int:id>/<string:name>', methods=['PUT'])
def worker_update(id, name=' ', speciality=' ', experience='0'):
    if Worker.is_exp(experience):
        w0 = Worker(id, name, speciality, experience)
        w = app.sql.worker_by_id(id)
        if not w:
            return 'Ошибка!\nУказанная запись не найдена.', 400
        if w.merge(w0) and app.sql.worker_update(w):
            return 'Работник обновлен!', 205
    return 'Ошибка!\nПроверьте запрос.', 400

@app.route('/workers/delete/<int:id>', methods=['POST'])
def worker_delete(id):
    if app.sql.worker_by_id(id) and app.sql.worker_delete(id):
        return 'Работник удален!', 205
    return 'Ошибка!\nПроверьте запрос.', 400


app.start()
