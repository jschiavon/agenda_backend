myuser = 'SA'
mypwd = 'Abcd1234'
myhost = '217.61.61.49'
myport = '1433'
mydb = 'PTR'

SQLALCHEMY_DATABASE_URI = f'mssql+pymssql://{myuser}:{mypwd}@{myhost}:{myport}/{mydb}'