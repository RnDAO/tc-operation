import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv
import json
import logging

from rndao_analyzer import RnDaoAnalyzer

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

    analyzer.set_database_info(
        db_url="",
        db_host=host,
        db_password=password,
        db_user=user,
        db_port=port
    )
    analyzer.database_connect()

    def do_GET(self):
        self.send_response(code=200)
        self.send_header(keyword='Content-type', value='application/json')
        self.end_headers()

        self.analyzer.run_once(None)

        json_to_pass = json.dumps({
            "status": "ok"
        })
        self.wfile.write(json_to_pass.encode('utf-8'))

        return


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
