import sqlite3

class Messages:
    def __init__(self):
        '''
            The constructor of the Messages class.
        '''
        self.con = sqlite3.connect('messages.sqlite')
        self.cur = self.con.cursor()
        sql = '''
            CREATE TABLE IF NOT EXISTS messages (
                user_id     INTEGER         NOT NULL,
                chat_id     INTEGER         NOT NULL,
                content     TEXT            NOT NULL,
                score       REAL            NOT NULL,
                technology  TEXT
            );
        '''
        self.cur.execute(sql)

    def insertOne(self, chat_id, user_id, content, score, technology=None):
        '''
            This function executes an INSERT query on the messages table
        :param chat_id: int
            The chat id were the message has been sent.
        :param user_id: int
            The id of the user who sent the message.
        :param content: str
            The content of the message.
        :param score: float
            The score that was given by the sentiment pipeline
        '''
        sql = 'INSERT INTO messages VALUES (?, ?, ?, ?, ?)'
        if technology is None:
            self.cur.execute(sql, (chat_id, user_id, content, score, 'non-tech'))
        else:
            self.cur.execute(sql, (chat_id, user_id, content, score, technology))
        self.con.commit()

    def readByUser(self, user_id):
        '''
            This function executes a SELECT statement on the messages table.
        :param user_id: int
            The id of the user who sent the message.
        :return: list
            A list of tuples that contains the messages columns.
        '''
        sql = 'SELECT * FROM messages WHERE user_id = (?)'
        self.cur.execute(sql, ( user_id, ))
        return self.cur.fetchall()

    def userMeanScore(self, user_id):
        '''
            This function executes a SELECT statement on the messages table.
        :param user_id: int
            The id of the user who sent the message.
        :return: float
            The mean value of the score column for a given user.
        '''
        sql = 'SELECT score FROM messages WHERE user_id = (?)'
        self.cur.execute(sql, ( user_id, ))
        scores = self.cur.fetchall()
        result = 0
        for score in scores:
            result += score[0]
        result /= len(scores)
        return result

    def __del__(self):
        '''
            The destructor of the Messages class.
        '''
        self.con.close()
