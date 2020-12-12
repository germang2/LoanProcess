from typing import Optional, Awaitable

from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json
from tornado.escape import json_decode, json_encode


class CheckLoan(RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        self.write(json.dumps({'message': 'hello from tornado'}))

    def post(self):
        body = json_decode(self.request.body)
        response = {}
        if 'amount' in body:
            decision = ''
            amount = body['amount']
            if amount > 50000:
                decision = 'DECLINE'
            elif amount == 50000:
                decision = 'UNDECIDED'
            else:
                decision = 'APPROVED'

            response['decision'] = decision
        self.write(json.dumps(response))

    def options(self):
        # no body
        self.set_status(204)
        self.finish()


def make_app():
    urls = [("/api/checkloan", CheckLoan)]
    return Application(urls, debug=True)


if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    IOLoop.instance().start()