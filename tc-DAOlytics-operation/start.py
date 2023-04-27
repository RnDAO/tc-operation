import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv
import json
import logging
# from urlparse import parse_qs
from urllib.parse import urlparse
from recompute_subprocess import popen_and_call, notify_backend

# from rndao_analyzer import RnDaoAnalyzer

PORT_NUMBER = 8080


# This class will handles any incoming request from
class AnalyzerHandler(BaseHTTPRequestHandler):

    analyzer = RnDaoAnalyzer()
    load_dotenv()

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

    neo4j_dbName = os.getenv("NEO4J_DB")
    neo4j_url = os.getenv("NEO4J_URI")
    neo4j_user = os.getenv("NEO4J_USER")
    neo4j_password = os.getenv("NEO4J_PASSWORD")

    analyzer.set_database_info(
        db_url="",
        db_host=host,
        db_password=password,
        db_user=user,
        db_port=port
    )
    analyzer.set_neo4j_utils(neo4j_dbName=neo4j_dbName,
                             neo4j_url=neo4j_url,
                             neo4j_auth=(neo4j_user, neo4j_password))

    ## mongoDB connection
    analyzer.database_connect()
    
    ## neo4j db connection
    analyzer.database_neo4j_connect()

    def do_GET(self):

        backend_url = os.getenv('NOTIFY_BACKEND_URL')
        backend_secret = os.getenv('BACKEND_API_KEY')

        self.send_response(code=200)
        self.send_header(keyword='Content-type', value='application/json')
        self.end_headers()

        _, _, path, _, query, _ = urlparse(self.path)

        if path == '/':
            self.analyzer.run_once(None)
            self.write_sccess()
        elif path == '/recompute_analytics':
            param = query.split('&')

            ## we're getting the id of guild from a string like: `guildId=1534654`
            if len(param_splition) == 2 and len(param) > 1:
                param_splition = param[0].split('=')
                guildId = param_splition[1]

                ## we need another thread not to block the api and run the analyzer 
                ## when it ends, it would call backend
                popen_and_call(on_exit=notify_backend, 
                            function=self.analyzer.recompute_analytics_on_guilds, 
                            inputs_function=guildId,
                            inputs_on_exit=(backend_url, backend_secret) )
                
                self.write_sccess()
            else:
                self.write_fail(extra_info="there must be just one parameter!")

        else:
            self.write_fail(extra_info="Path Not found!")

        return

    def write_sccess(self):
        json_to_pass = json.dumps({
            "status": "ok"
        })
        self.wfile.write(json_to_pass.encode('utf-8'))
    
    def write_fail(self, extra_info=None):
        json_to_pass = json.dumps({
            "status": "404",
            "extra_info": extra_info
        })
        self.wfile.write(json_to_pass.encode('utf-8'))


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), AnalyzerHandler)
    print('Started httpserver on port ', PORT_NUMBER)

    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
