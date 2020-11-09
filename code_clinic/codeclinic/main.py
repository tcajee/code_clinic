
import os
from tinydb import TinyDB
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from cement.utils import fs
from .core.exc import CodeClinicError
from .controllers.base import Base
from .controllers.bookings import Bookings

# configuration defaults
CONFIG = init_defaults('codeclinic')
CONFIG['codeclinic']['db_file'] = '~/.codeclinic/db.json'
CONFIG['codeclinic']['email'] = 'tcajee@student.wethinkcode.co.za'

def extend_tinydb(app):
    app.log.info('Extending codeclinic application with TinyDB')
    db_file = app.config.get('codeclinic', 'db_file')

    # Ensure full path expansion
    db_file = fs.abspath(db_file)
    app.log.info(f"Full path to db_file: {db_file}")

    # Ensure parent directory exists
    db_dir = os.path.dirname(db_file)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    app.extend('db', TinyDB(db_file))


class CodeClinic(App):
    """Code Clinic primary application."""

    class Meta:
        label = 'codeclinic'

        # Configuration defaults
        config_defaults = CONFIG

        # Call sys.exit() on close
        exit_on_close = True

        # Load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # Configuration handler
        config_handler = 'yaml'

        # Configuration file suffix
        config_file_suffix = '.yml'

        # Set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # Register handlers
        handlers = [
            Base,
            Bookings,
        ]

        # Register hooks
        hooks = [
            ('post_setup', extend_tinydb)
        ]


class CodeClinicTest(TestApp,CodeClinic):
    """A sub-class of CodeClinic that is better suited for testing."""

    class Meta:
        label = 'codeclinic'


def main():
    with CodeClinic() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CodeClinicError as e:
            print('CodeClinicError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
