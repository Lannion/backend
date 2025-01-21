from django.core.management.base import BaseCommand
import MySQLdb
from django.conf import settings

class Command(BaseCommand):
    help = 'Creates the database if it does not exist'

    def handle(self, *args, **kwargs):
        db_name = settings.DATABASES['default']['NAME']
        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        host = settings.DATABASES['default']['HOST']

        # Connect to MySQL (without specifying a database)
        conn = MySQLdb.connect(user=user, password=password, host=host)
        cursor = conn.cursor()

        # Create the database
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
        self.stdout.write(self.style.WARNING(f'Database {db_name} dropped successfully'))

        # Close the connection
        cursor.close()
        conn.close()