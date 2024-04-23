import logging
from types import SimpleNamespace
import pymysql
from pymysql import cursors
from flask import current_app, g

logger = logging.getLogger(__name__)


class MySQL(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the `app` for use with this
        :class:`~flask_pymysql.MySQL` class.
        This is called automatically if `app` is passed to
        :meth:`~MySQL.__init__`.

        :param flask.Flask app: the application to configure for use with
            this :class:`~flask_pymysql.MySQL` class.
        """

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)

    @property
    def connect(self):
        if current_app.config['FLASK_PYMYSQL_KWARGS']:
            kwargs = current_app.config['FLASK_PYMYSQL_KWARGS']
            if 'cursorclass' in kwargs.keys():
                if isinstance(kwargs['cursorclass'], str):
                    kwargs['cursorclass'] = getattr(cursors, kwargs['cursorclass'])
        else:
            kwargs = dict()

        return pymysql.connect(**kwargs)

    @property
    def connection(self):
        """Attempts to connect to the MySQL server.

        :return: Bound MySQL connection object if successful or ``None`` if
            unsuccessful.
        """

        try:
            g._mysql = SimpleNamespace()
            g._mysql.connection = self.connect
            logger.debug("FLASK-PYMYSQL successfully created MySQL connection")
            return g._mysql.connection
        except Exception as ex:
            logger.exception("Could not create MySQL connection", exc_info=ex)
            return None

    def teardown(self, exception):
        if hasattr(g, '_mysql') and g._mysql.connection:
            g._mysql.connection.close()
            logger.debug("FLASK-PYMYSQL successfully closed MySQL connection")
