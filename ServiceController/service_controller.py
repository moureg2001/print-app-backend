from __future__ import annotations
import os
from abc import ABC
import azure.functions as func
import tempfile
from .config import config

from ServiceController.user_data import User, Keychain


def create_dir_in_temp():
    tempFilePath = tempfile.gettempdir()
    fp = tempfile.NamedTemporaryFile()


class ServiceMediator(ABC):
    def notify(self, sender: object, event: str, data: None) -> None:
        """The required notify method"""

    def response(self, event: str):
        """The required receive method"""


class ConcreteMediator(ServiceMediator):
    def __init__(self, user_data_service, blob_file_service,
                 blob_logo_service, email_service, processing_service) -> None:
        self.data = dict
        self.user_data_service = user_data_service
        self.user_data_service.mediator = self
        self.blob_file_service = blob_file_service
        self.blob_file_service.mediator = self
        self.blob_logo_service = blob_logo_service
        self.blob_logo_service.mediator = self
        self.email_service = email_service
        self.email_service.mediator = self
        self.processing_service = processing_service
        self.processing_service.mediator = self

    def extract_data(self, data):
        new_keychain = Keychain(data['keychain']['text'], data['keychain']['logo'])
        # print(new_keychain)
        new_user = User(data['surname'], data['name'],
                        data['email'], data['company'],
                        data['department'], data['phone'],
                        data['role'], new_keychain)
        return new_user

    def save_file_for_processing(self, blob, filepath):  # it save the logo and scad file on PROCESSING_DIRECTORY
        with open(filepath, "wb") as file:
            file.write(blob)

    def notify(self, sender: object, event: str, data: None) -> None:
        print("notify started ...")
        if not (data is None):
            self.data = data
            user = self.extract_data(self.data)
        else:
            print(self.data)
            user = self.extract_data(self.data)

        if event == "R":  # Rest Services
            print("Mediator reacts on R and triggers following operations: -> Rest Services")

        elif event == "D":  # Data Services
            print("Mediator reacts on D and triggers following operations: -> Data Services")
            self.user_data_service.insert_user_obj_data(user)

        elif event == "B":  # Blob Service
            print("Mediator reacts on B and triggers following operations: -> Blob Service")
            scad_relative_path = "ProcessingService/PROCESSING_DIRECTORY/keychain.scad"
            if os.path.isfile(scad_relative_path):
                os.remove(scad_relative_path)
            self.save_file_for_processing(self.blob_file_service.download_file("keychain.scad"), scad_relative_path)
            print("logo:" + user.keychain.logo)
            if user.keychain.logo:
                logo_relative_path = f"ProcessingService/PROCESSING_DIRECTORY/{user.keychain.logo}.svg"
                self.save_file_for_processing(self.blob_logo_service.download_file(user.keychain.logo + ".svg"),
                                              logo_relative_path)
            else:
                self.blob_logo_service.download_void()



        elif event == "P":  # Processing Service
            print("Mediator reacts on P and triggers following operations: -> Processing Service"
                  "\n Converting .scad file to stl, saving the "
                  ".stl file on ATTACHMENT folder to send it as attachment with the Email ")
            self.processing_service.name = user.keychain.text
            self.processing_service.logo = user.keychain.logo + ".svg"
            scad_filepath = "ProcessingService/PROCESSING_DIRECTORY/keychain_out.scad"
            stl_filepath = "EmailService/ATTACHMENT/keychain.stl"
            self.processing_service.scad_stl_converter(scad_filepath, stl_filepath)
            # self.blob_file_service.upload_file(stl_filepath, os.path.basename(stl_filepath))

        elif event == "E":  # Email Service
            print("Mediator reacts on E and triggers following operations: Sending Email")

            # if self.filename is not None:
            #     self.add_attachment(self.filename)
            # else:
            #     self.filename = config['file_path']
            #     self.add_attachment(self.filename)
            self.email_service.login_send_email()
            os.remove(config['file_path'])


class ServiceBaseController:
    """
    The Mediator interface declares a method used by components to notify the
    mediator about various events. The Mediator may react to these events and
    pass the execution to other components.
    """

    def __init__(self, mediator: ServiceMediator = None) -> None:
        from DataService.userdataservice import UserDataServiceBase
        from BlobManager.blob_service import AzureBlobFileService, AzureBlobLogoService
        from EmailService.email_sender import EmailSender
        from ProcessingService.process_service import ProcessingServiceBase
        data_service = UserDataServiceBase()
        blob_file_service = AzureBlobFileService()
        blob_logo_service = AzureBlobLogoService()
        email_service = EmailSender(config['subject'], config['body'], None)
        processing_service = ProcessingServiceBase()
        self._mediator = ConcreteMediator(data_service, blob_file_service,
                                          blob_logo_service, email_service, processing_service)

    @property
    def mediator(self) -> ServiceMediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: ServiceMediator) -> None:
        self._mediator = mediator
