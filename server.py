import torndb
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
from binascii import hexlify
from tornado.options import define, options

define("port", default=1104, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="test", help="database name")
define("mysql_user", default="x", help="database user")
define("mysql_password", default="y", help="database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            #get
             (r"/login/([^/]+)/([^/]+)", login),
             (r"/logout/([^/]+)/([^/]+)", logout),
             (r"/sendticket/([^/]+)/([^/]+)/([^/]+)", sendticket),
             (r"/getticketcli/([^/]+)", getticketcli),
             (r"/closeticket/([^/]+)/([^/]+)", closeticket),
             (r"/getticketmod/([^/]+)", getticketmod),
             (r"/restoticketmod/([^/]+)/([^/]+)/([^/]+)", restoticketmod),
             (r"/changestatus/([^/]+)/([^/]+)/([^/]+)", changestatus),
             (r"/signup/([^/]+)/([^/]+)/([^/]+)/([^/]+)/([^/]+)", signup),
            #post
            (r"/login", login),
            (r"/signup", signup),
            (r"/logout", logout),
            (r"/sendticket", sendticket),
            (r"/getticketcli", getticketcli),
            (r"/closeticket", closeticket),
            (r"/getticketmod", getticketmod),
            (r"/restoticketmod", restoticketmod),
            (r"/changestatus", changestatus),
            (r".*", defaulthandler),
        ]
        settings = dict()
        super(Application, self).__init__(handlers, **settings)
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def check_user(self, user):
        resuser = self.db.get("SELECT * from user where username = %s", user)
        if resuser:
            return True
        else:
            return False

    def check_api(self, api):
        resuser = self.db.get("SELECT * from user where token = %s", api)
        if resuser:
            return True
        else:
            return False

    def return_user(self, api):
        resuser = self.db.get("SELECT * from user where token = %s", api)
        if resuser:
            return resuser
        else:
            return False

    def check_auth(self,username,password):
        resuser = self.db.get("SELECT * from user where username = %s and password = %s", username,password)
        if resuser:
            return True
        else:
            return False

class defaulthandler(BaseHandler):
    def get(self):
        output = {'message': 'Wrong Command',
                  'status':'false'}
        self.write(output)

    def post(self):
        output = {'message': 'Wrong Command',
                  'status':'false'}
        self.write(output)


class signup(BaseHandler):
    def get(self,*args):
        t = self.check_user(args[0])
        if not t:
            api_token = str(hexlify(os.urandom(16)))
            user_id = self.db.execute("""INSERT INTO user (username, password,firstname,lastname, token,rule) values (%s,%s,%s,%s,%s,%s) """, args[0],args[1],args[2],args[3], api_token,args[4])

            output = {'message': 'signed up Successfully',
                      'code': '200',
                      'api': api_token,
                      'status': 'OK'}
            self.write(output)
        else:
            output = {'message': 'User Exist',
                      'status': 'false'}
            self.write(output)

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        firstname = self.get_argument('firstname')
        lastname = self.get_argument('lastname')
        rule = self.get_argument('rule')
        t = self.check_user(username)
        if not t:
            api_token = str(hexlify(os.urandom(16)))
            user_id = self.db.execute(
                """INSERT INTO user (username, password,firstname,lastname, token,rule) values (%s,%s,%s,%s,%s,%s) """,
                username, password, firstname, lastname, api_token, rule)

            output = {'message': 'signed up Successfully',
                      'code': '200',
                      'api': api_token,
                      'status': 'OK'}
            self.write(output)
        else:
            output = {'message': 'User Exist',
                      'status':'false'}
            self.write(output)


class login(BaseHandler):
    def get(self, *args):
        t = self.check_auth(args[0], args[1])
        if t:
            api_token = str(hexlify(os.urandom(16)))
            user_id = self.db.execute("""update user set token = %s where username= %s""", api_token,args[0])

            output = {'message': 'logged in Successfully',
                      'code': '200',
                      'api': api_token,
                      'status': 'OK'}
            self.write(output)
        else:
            output = {'message': 'User Exist',
                      'status': 'false'}
            self.write(output)

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        t = self.check_auth(username, password)
        if t:
            api_token = str(hexlify(os.urandom(16)))
            user_id = self.db.execute("""update user set token = %s where username= %s""", api_token, username)

            output = {'message': 'logged in Successfully',
                      'code': '200',
                      'api': api_token,
                      'status': 'OK'}
            self.write(output)
        else:
            output = {'message': 'User Exist',
                      'status': 'false'}
            self.write(output)


class logout(BaseHandler):
    def get(self,*args):
        t = self.check_auth(args[0], args[1])
        if t:
            api_token = ""
            user_id = self.db.execute("""update user set token = %s where username= %s""", api_token,args[0])

            output = {'message': 'logged out Successfully',
                      'code': '200',
                      'status': 'OK'}
            self.write(output)
        else:
            output = {'message': 'Wrong username or password',
                      'status': 'false'}
            self.write(output)

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        t = self.check_auth(username, password)
        if t:
            api_token = ""
            user_id = self.db.execute("""update user set token = %s where username= %s""", api_token, username)

            output = {'message': 'logged out Successfully',
                      'code': '200',
                      'status': 'OK'}
            self.write(output)
        else:
            output = {'message': 'Wrong username or password',
                      'status': 'false'}
            self.write(output)


class sendticket(BaseHandler):
    def get(self,*args):
        t = self.check_api(args[0])
        sender = self.return_user(args[0])
        if t:
            user_id = self.db.execute("""INSERT INTO tickets (subject, body,situation,sender,reciver) values (%s,%s,%s,%s,%s) """, args[1], args[2], "open",sender["username"],sender["username"])

            output = {'message': 'ticket sent Succsessfully',
                      'code': '200',
                      'status': 'OK'}
            self.write(output)
        else:
            output = {'message': 'Wrong api',
                      'status': 'false'}
            self.write(output)

    def post(self, *args, **kwargs):
            token = self.get_argument('token')
            subject = self.get_argument('subject')
            body = self.get_argument('body')
            t = self.check_api(token)
            sender = self.return_user(token)
            if t:
                user_id = self.db.execute("""INSERT INTO tickets (subject, body,situation,sender,reciver) values (%s,%s,%s,%s,%s) """,
                                          subject, body, "open", sender["username"], sender["username"])

                output = {'message': 'ticket sent Succsessfully',
                          'code': '200',
                          'status': 'OK'}
                self.write(output)
            else:
                output = {'message': 'Wrong api',
                          'status': 'false'}
                self.write(output)


class getticketcli(BaseHandler):
    def get(self, *args):
        t = self.check_api(args[0])
        user = self.return_user(args[0])
        if t:
            user_id = self.db.query("SELECT * from tickets where reciver=%s", user["username"])
            temp_o = {}
            output = {'message': 'your tickets are ready for show :',
                      'code': '200',
                      'status': 'OK',
                      'blocks': {}
                      }
            for x in range(0, len(user_id)):
                temp_o[x] = {
                    'subject': user_id[x]["subject"],
                    'body': user_id[x]["body"],
                    'status': user_id[x]["situation"],
                    'id': user_id[x]["id"],
                }
                output['blocks'].update(temp_o)

            self.write(output)
        else:
            output = {'message': 'Wrong api',
                      'status': 'false'}
            self.write(output)

    def post(self):
            token = self.get_argument('token')
            t = self.check_api(token)
            user = self.return_user(token)
            if t:
                user_id = self.db.query("""select * from tickets where reciver=%s""", user["username"])
                temp_o = {}
                output = {'message': 'your tickets are ready for show :',
                          'code': '200',
                          'status': 'OK',
                          'blocks': {}
                          }

                for x in range(0,len(user_id)) :
                    temp_o[x]={
                        'subject' : user_id[x]["subject"],
                        'body': user_id[x]["body"],
                        'status': user_id[x]["situation"],
                        'id': user_id[x]["id"],
                    }
                    output['blocks'].update(temp_o)

                self.write(output)
            else:
                output = {'message': 'Wrong api',
                          'status': 'false'}
                self.write(output)


class closeticket(BaseHandler):
    def get(self,*args):
        t = self.check_api(args[0])
        user = self.return_user(args[0])
        x = "close"
        if t:
            user_id = self.db.execute("""update tickets set situation =%s where id=%s """,x,args[1])
            output = {'message': 'ticket closed Succsessfully',
                      'code': '200',
                      'status': 'OK'}
            self.write(output)
        else:
            output = {'message': 'Wrong api',
                      'status': 'false'}
            self.write(output)

    def post(self):
        token = self.get_argument('token')
        id_2 = self.get_argument('id')
        t = self.check_api(token)
        sender = self.return_user(token)
        if t:
            user_id = self.db.execute("""update tickets set situation = %s where id= %s""", "close", id_2[0])
            output = {'message': 'ticket closed Succsessfully',
                      'code': '200',
                      'status': 'OK'}
            self.write(output)
        else:
            output = {'message': 'Wrong api',
                      'status': 'false'}
            self.write(output)


class getticketmod(BaseHandler):
    def get(self, *args):
        user = self.return_user(args[0])
        y = "admin"
        if user["rule"] == y:
            user_id = self.db.query("SELECT * from tickets ")
            temp_o = {}
            output = {'message': 'tickets are ready to show :',
                      'code': '200',
                      'status': 'OK',
                      'blocks': {}
                      }
            for x in range(0, len(user_id)):
                temp_o[x] = {
                    'subject': user_id[x]["subject"],
                    'body': user_id[x]["body"],
                    'status': user_id[x]["situation"],
                    'id': user_id[x]["id"],
                }
                output['blocks'].update(temp_o)
                self.write(output)
        else:
            output = {'message': 'Wrong api',
                      'status': 'false'}
            self.write(output)

    def post(self):
            token = self.get_argument('token')
            t = self.check_api(token)
            user = self.return_user(token)
            y = "admin"
            if user["rule"] == y:
                user_id = self.db.query("""select * from tickets """)
                temp_o = {}
                output = {'message': 'tickets are ready to show :',
                          'code': '200',
                          'status': 'OK',
                          'blocks': {}
                          }
                for x in range(0, len(user_id)):
                    temp_o[x] = {
                        'subject': user_id[x]["subject"],
                        'body': user_id[x]["body"],
                        'status': user_id[x]["situation"],
                        'id': user_id[x]["id"],
                    }
                    output['blocks'].update(temp_o)
                self.write(output)
            else:
                output = {'message': 'Wrong api',
                          'status': 'false'}
                self.write(output)


class restoticketmod(BaseHandler):
    def get(self,*args):
        user = self.return_user(args[0])
        y = "admin"
        if user["rule"] == y:
            user_id = self.db.get("""select sender from tickets  where id=%s """, args[1])
            user_id2 = self.db.execute("""insert into tickets (sender,reciver,body,situation,subject) values (%s,%s,%s,%s,%s) ""","admin",user_id["sender"],args[2],"open","Answer")
            output = {'message': 'response sent successully',
                      'code': '200',
                      'status': 'OK'}
            self.write(output)
        else:
            output = {'message': 'Wrong api',
                      'status': 'false'}
            self.write(output)

    def post(self, *args, **kwargs):
            token = self.get_argument('token')
            id_2 = self.get_argument('id')
            body = self.get_argument('body')
            t = self.return_user(token)
            y = "admin"
            if t["rule"] == y:
                user_id = self.db.get("""select sender from tickets  where id=%s """, id_2)
                user_id2 = self.db.execute(
                    """insert into tickets (sender,reciver,body,situation,subject) values (%s,%s,%s,%s,%s) """, "admin", user_id["sender"],
                    body, "open","Answer")

                output = {'message': 'response sent Succsessfully',
                          'code': '200',
                          'status': 'OK'}
                self.write(output)
            else:
                output = {'message': 'Wrong api',
                          'status': 'false'}
                self.write(output)


class changestatus(BaseHandler):
    def get(self,*args):
        user = self.return_user(args[0])
        y = "admin"
        if user["rule"] == y:
            user_id = self.db.execute("""update tickets set situation= %s where id = %s""", args[2],args[1])

            output = {'message': 'status changed Successfully',
                      'code': '200',
                      'status': 'OK'}
            self.write(output)
        else:
            output = {'message': 'Wrong username or password',
                      'status': 'false'}
            self.write(output)

    def post(self, *args, **kwargs):
        token = self.get_argument('token')
        id_2 = self.get_argument('id')
        status = self.get_argument('status')
        user = self.return_user(token)
        y = "admin"
        if user["rule"] == y:
            user_id = self.db.execute("""update tickets set situation= %s where id = %s""", status, id_2)

            output = {'message': 'status changed Successfully',
                      'code': '200',
                      'status': 'OK'}
            self.write(output)
        else:
            output = {'message': 'Wrong username or password',
                      'status': 'false'}

            self.write(output)



def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
