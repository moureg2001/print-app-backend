import logging as log
import shortuuid as suuid
import logging
from azure.core.exceptions import ResourceExistsError, HttpResponseError
from azure.data.tables import TableServiceClient
from .config import config
from ServiceController.service_controller import ServiceBaseController

# Create a logger for the 'azure' SDK
logger = logging.getLogger('azure')
logger.setLevel(logging.DEBUG)


class UserDataServiceBase(ServiceBaseController):
    def __init__(self):
        """Initialize the connection to Azure storage account"""
        self.table_service = TableServiceClient.from_connection_string(
            conn_str=config['azure_storage_connection_string'],
            logging_enable=True)
        self.__tablename__ = "users"

    def insert_user_obj_data(self, user_data_service) -> None:
        try:
            self.table_service.create_table_if_not_exists(self.__tablename__)
        except HttpResponseError:
            print("Table already exists")
        print(user_data_service)
        try:
            user_id = suuid.uuid()
            user_name = f"{user_data_service.surname.capitalize()}{user_data_service.name.capitalize()}{user_id}"
            user_entity = {
                u'PartitionKey': user_name,
                u'RowKey': user_id,
                u'surname': user_data_service.surname,
                u'name': user_data_service.name,
                u'email': user_data_service.email,
                u'company': user_data_service.company,
                u'department': user_data_service.department,
                u'phone': user_data_service.phone,
                u'role': user_data_service.role
            }
            table_client = self.table_service.get_table_client(table_name=self.__tablename__)
            user_model_entity = table_client.create_entity(entity=user_entity)
        except ResourceExistsError:
            print("Entity already exists")

    def insert_user_data(self, surname: str, name: str, email: str, company: str = None,
                         department: str = None, phone: str = None, role: str = None) -> None:
        log.info("UserDataService insert data to Table Storage")
        try:
            self.table_service.create_table_if_not_exists(self.__tablename__)
        except HttpResponseError:
            print("Table already exists")
        try:
            user_id = suuid.uuid()
            user_name = f"{surname.capitalize()}{name.capitalize()}{user_id}"

            user_entity = {
                u'PartitionKey': user_name,
                u'RowKey': user_id,
                u'surname': surname,
                u'name': name,
                u'email': email,
                u'company': company,
                u'department': department,
                u'phone': phone,
                u'role': role
            }
            table_client = self.table_service.get_table_client(table_name=self.__tablename__)
            user_model_entity = table_client.create_entity(entity=user_entity)
        except ResourceExistsError:
            print("Entity already exists")
