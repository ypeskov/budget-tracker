class BackupPostgresDbError(Exception):
    """ Custom exception for backup_postgres_db function """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
