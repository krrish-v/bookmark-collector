
import sqlite3

def reverse(lst):
    data = {}
    print(lst)
    for ele in reversed(lst):

        if ele[1] in data:
            data[ele[1]].append(ele[0])
        else: data[ele[1]] = [ele[0]]
    
    return data


class get_db():
    def __init__(self):
        self.conn_ = sqlite3.connect('database/databse.db')

    def in_db(self, useremail, password):
        self.useremail = useremail
        self.password = password

        try:
            cursor = self.conn_.cursor()
            #cursor.execute('create table search (useremail text not null, password text not null)')
            cursor.execute("insert into search values(?, ?)", (self.useremail, self.password))
            self.conn_.commit()
            self.conn_.close()
            return True
        
        except: return False

    def add_bookmark_db(self, useremail):
        self.useremail = useremail

        self.useremail = self.useremail.replace('@', '_')
        self.useremail = self.useremail.replace('.', '_')

        try:

            cursor = self.conn_.cursor()
            command = 'create table ' + self.useremail + ' (link text not null, tags text not null)'
            cursor.execute(command)
            self.conn_.close()
        except: return False

    def add_link(self, useremail, link, tags):
        self.useremail = useremail
        self.link = link
        self.tags = tags

        self.useremail = self.useremail.replace('@', '_')
        self.useremail = self.useremail.replace('.', '_')
        
        cursor = self.conn_.cursor()

        command = "insert into " + self.useremail + " values(?, ?)"
        
        cursor.execute(command, (self.link, self.tags))

        self.conn_.commit()
        self.conn_.close()

    def out_db(self, useremail):

        self.useremail = useremail
        self.useremail = self.useremail.replace('@', '_')
        self.useremail = self.useremail.replace('.', '_')
        
        try:
            cursor = self.conn_.cursor()

            command = "select link, tags from " + self.useremail
            cursor.execute(command)

            data = cursor.fetchall()
            self.conn_.close()
            
            if len(data) != 0:
                # reverse the list
                data_ = reverse(data)
                return data_
            else:
                return []

        except: return []


#print(get_db().in_db('helo@gmail.com', 'eviu3ik3v'))
#print(get_db().add_bookmark_db('helo@gmail.com'))
#print(get_db().add_link('helo@gmail.com', 'https://discord.com', 'socila media'))
#print(get_db().out_db('helo@gmail.com'))
