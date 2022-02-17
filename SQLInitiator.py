import mysql.connector


class SQLInitiator:
    cnx = mysql.connector.connect(
          host="localhost",
          user="root",
          password="root",
          database="maman_db"
        );

    def executeScriptsFromFile(self,filename):
        fd = open(filename, 'r')
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split(';')

        for command in sqlCommands:
            try:
                if command.strip() != '':
                    self.cnx.cursor().execute(command);
            except IOError as msg:
                print("Command skipped: ", msg);

    def setSQLEnv(self):

        self.executeScriptsFromFile('db_scripts/server.db');
        self.cnx.commit();
        return self.cnx;

    def resetDB(self):

        self.executeScriptsFromFile('db_scripts/clearDB.db');
        self.cnx.commit();
        return self.cnx;

if __name__ == '__main__':

    sql = SQLInitiator();
    conn = sql.setSQLEnv();

