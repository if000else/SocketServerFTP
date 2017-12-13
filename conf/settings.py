from pathlib import Path
BASEDIR = Path(__file__).parent.parent

LogPath = str(BASEDIR / "logs")
###USER
USER_DATA = str(BASEDIR / "database" / "users")

###database
DATABASE = str(BASEDIR / "database")


###SEVER
HomeOfServer = str(BASEDIR / "database" / "server")

###socket
ADDR = '127.0.0.1'
PORT = 1212
MAXSIZE = 10240  #10M
TMOUT = 600 #10min
MAXCONN = 5 # max connecting amount
