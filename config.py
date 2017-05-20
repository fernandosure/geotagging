import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    MONGO_URI = os.environ.get('MONGO_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret#2017'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # #email errors to the administrators
        # import logging
        # from logging.handlers import SMTPHandler
        # credetials = None
        # secure = None

        # if getattr(cls, 'MAIL_USERNAME', None) is not None:
        #     credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)

        # if getattr(cls, 'MAIL_USE_TLS', None):
        #     secure = ()

        # mail_handler = SMTPHandler(
        #     mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
        #     fromaddr=cls.MAIL_SENDER,
        #     toaddrs=[cls.USER_ADMIN],
        #     subject=cls.MAIL_SUBJECT_PREFIX + ' Application Error',
        #     credentials=credentials,
        #     secure=secure)

        # mail_handler.setLevel(logging.ERROR)
        # app.logger.addHandler(mail_handler)






        


class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        #log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

        #handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))



class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        #log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'unix': UnixConfig,
    'default': DevelopmentConfig
}