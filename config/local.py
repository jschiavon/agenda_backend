myuser = 'SA'
mypwd = 'Abcd_1234'
myhost = 'localhost'
myport = '1433'
mydb = 'PTR'

SQLALCHEMY_DATABASE_URI = f'mssql+pymssql://{myuser}:{mypwd}@{myhost}:{myport}/{mydb}'