import os
import platform


def get_postgres_url(db_name='sick_bastard'):
    """
    Method returns current app database uri
    """

    url = os.getenv('INVOKE_DB_POSTGRES_URI')
    system = platform.system()
    if not url:
        # SANYA, ZA CHTO
        if system == 'Darwin':
            url = 'postgresql://localhost:5432/'
        else:
            url = 'postgresql://postgres:postgres@localhost:5432/'

    if url.endswith('/'):
        url = url + db_name

    return url
