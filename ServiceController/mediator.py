from abc import ABCMeta, abstractmethod

from ServiceController.user_data import User, Keychain


class IService(metaclass=ABCMeta):

    def __init__(self, med, name_):
        self.mediator = med
        self.name = name_

    @staticmethod
    @abstractmethod
    def notify(msg):
        """The required notify method"""

    @staticmethod
    @abstractmethod
    def receive(msg):
        """The required receive method"""


class ServiceMediator(IService):
    """The Mediator Concrete (Implementation) Class"""

    def __init__(self):
        self.services = []

    def extract_data(self, data):
        new_keychain = Keychain(data['keychain']['text'], data['keychain']['logo'])
        new_user = User(data['surname'], data['name'],
                        data['email'], data['company'],
                        data['department'], data['phone'],
                        data['role'], new_keychain)
        return new_user

    def add_service(self, service):
        self.services.append(service)

    def notify(self, message, service):
        for _service in self.services:
            _service.receive(message)

    @staticmethod
    def receive(msg):
        pass
#
#
# class ServiceMediator(metaclass=ABCMeta):
#     def notify(self, sender: object, event: str) -> None:
#         """The required notify method"""
#
#
# class ConcreteMediator(ServiceMediator):
#     def __init__(self, data_controller: DataController, user_data_service: UserDataService,
#                  email_controller: EmailController, processing_controller: ProcessingController,
#                  rest_front_backend_service: RestFrontBackendService):
#         self.data_controller = data_controller
#         self.data_controller.mediator = self
#         self.user_data_service = user_data_service
#         self.user_data_service.mediator = self
#         self.email_controller = email_controller
#         self.email_controller.mediator = self
#         self.processingController = processing_controller
#         self.processingController.mediator = self
#         self.rest_front_backend_service = rest_front_backend_service
#         self.rest_front_backend_service.mediator = self
#
#     def extract_data(self, data):
#         new_keychain = Keychain(data['keychain']['text'], data['keychain']['logo'])
#         new_user = User(data['surname'], data['name'],
#                         data['email'], data['company'],
#                         data['department'], data['phone'],
#                         data['role'], new_keychain)
#         return new_user
#
#     def notify(self, sender: object, event: str) -> None:
#         user = self.extract_data(self.rest_front_backend_service.data)
#         if event == "R":  # Rest Services
#             print("Mediator reacts on R and triggers following operations:")
#             self.rest_front_backend_service.post()
#         elif event == "D":  # Data Services
#             print("Mediator reacts on D and triggers following operations:")
#             self.user_data_service.insert_user_data(user)
#         elif event == "B":  # Blob Service
#             print("Mediator reacts on B and triggers following operations:")
#             self._component1.do_b()
#             self._component2.do_c()
#         elif event == "E":  # Email Service
#             print("Mediator reacts on E and triggers following operations:")
#             self._component1.do_b()
#             self._component2.do_c()
#         elif event == "P":  # Processing Service
#             print("Mediator reacts on P and triggers following operations:")
#             self._component1.do_b()
#             self._component2.do_c()
