create_table_command = ("create table if not exists status (\n"
                        "id integer primary key, \n"
                        "name text not null, \n"
                        "status text not null, \n"
                        "updated timestamp not null)")
DB_NAME = 'telemetry'
STATUS_TABLE = 'status'
STATUS_COLUMNS = ['name', 'status', 'updated']
telemetry_serial = '/dev/pts/2'
telemetry_serial_rate = 9600
GET_STATUS_OPERATION = '[status]'
