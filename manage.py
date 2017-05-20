import os
from app import create_app, mongo
from flask_script import Manager, Shell
from flask import url_for

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, mongo=mongo)

manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.option('-h', '--host', dest='host', default='0.0.0.0')
@manager.option('-p', '--port', dest='port', type=int, default=5000)
@manager.option('-w', '--workers', dest='workers', type=int, default=10)
@manager.option('-t', '--timeout', dest='timeout', type=int, default=90)
def gunicorn(host, port, workers, timeout):
    """Start the Server with Gunicorn"""
    from gunicorn.app.base import Application

    class FlaskApplication(Application):
        def init(self, parser, opts, args):
            return {
                'bind': '{0}:{1}'.format(host, port),
                'workers': workers, 'timeout': timeout

            }

        def load(self):
            return app

    application = FlaskApplication()
    return application.run()


@manager.command
def profile(length=25, profile_dir=None):
    """Start de application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
    app.run()


@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print line

if __name__ == '__main__':
    manager.run()
