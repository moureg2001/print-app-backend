import logging as log
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import ServiceController.service_controller as sc
from flask_cors import CORS
# https://stkeychainprintwebsite.z6.web.core.windows.net/
app = Flask(__name__)
CORS(app)
api = Api(app)


class RestFrontBackendServiceBase(Resource, sc.ServiceBaseController):

    data = dict()

    @property
    def data(self):
        return self.data

    def post(self) -> None:
        print("RestService collect data from backend")
        root_parser = reqparse.RequestParser(bundle_errors=True)
        root_parser.add_argument('surname', type=str, help="surname is required", required=True)
        root_parser.add_argument('name', type=str, help="name is required", required=True)
        root_parser.add_argument('email', type=str, help="email is required", required=True)
        root_parser.add_argument('company', type=str, required=False)
        root_parser.add_argument('department', type=str, required=False)
        root_parser.add_argument('phone', type=str, required=False)
        root_parser.add_argument('role', type=str, required=False)
        root_parser.add_argument('keychain', type=dict)
        root_args = root_parser.parse_args()
        data = root_args
        self.mediator.notify(self, "D", data)
        self.mediator.notify(self, "B", data)
        return root_args, 201


api.add_resource(RestFrontBackendServiceBase, '/keychain/api/v1.0/users')



if __name__ == '__main__':
    app.run(debug=True)
