import os, yaml, logging as log
from azure.storage.blob import BlobServiceClient, BlobClient, BlobProperties
from azure.storage.blob import ContentSettings, ContainerClient
from abc import ABC, abstractmethod
from .config import config

from ServiceController.service_controller import ServiceBaseController


class BlobStorageService(ABC, ServiceBaseController):
    connection_string = config["azure_storage_connection_string"]
    container_name = str

    @abstractmethod
    def __init__(self):
        # Initialize the connection to Azure storage account
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = ContainerClient.from_connection_string(
            conn_str=config["azure_storage_connection_string"],
            container_name=self.container_name)

    @abstractmethod
    def upload_file(self, file, filename):
        pass

    @abstractmethod
    def download_file(self, filename):
        pass

    @abstractmethod
    def delete(self, filename):
        pass

    @abstractmethod
    def list_blobs(self):
        pass

    @abstractmethod
    def find_blob(self, filename):
        pass


class AzureBlobFileService(BlobStorageService):
    # Replace with blob container. This should be already created in azure storage.

    def __init__(self):
        print("Initializing AzureBlobFileUploader")
        # Initialize the connection to Azure storage account
        BlobStorageService.container_name = config["stl_container_name"]
        BlobStorageService.__init__(self)

    def upload_file(self, file, filename):
        """Uploading files to blob storage..."""
        log.info("Uploading files to blob storage...")
        blob_client = self.container_client.get_blob_client(filename)
        blob_client.upload_blob(file)
        print(f"{filename} upload to blob storage")

    def download_file(self, filename):
        """Download file from blob storage"""
        blob_client = self.container_client.get_blob_client(filename)
        file_blob = blob_client.download_blob().readall()
        return file_blob

    def delete(self, filename):
        self.container_client.delete_blob(filename)
        print(f"{filename} delete from blob storage")

    def list_blobs(self):
        print("\nListing blobs...")
        blobs = []
        # List the blobs in the container
        blob_list = self.container_client.list_blobs()
        blobs = [blob for blob in blob_list]
        # print(blobs)
        return blobs

    def find_blob(self, filename):
        # List the blobs in the container
        blob_list = self.container_client.list_blobs()
        for blob in blob_list:
            if blob.name == filename:
                return blob

    def extract_blob_info(self, filename):
        return self.find_blob(filename)


class AzureBlobLogoService(BlobStorageService):
    # Usually starts with DefaultEndpointsProtocol=https;...

    def __init__(self):
        print("Initializing AzureBlobFileUploader")
        # Initialize the connection to Azure storage account
        BlobStorageService.container_name = config["logo_container_name"]
        BlobStorageService.__init__(self)

    def upload_file(self, file, filename):
        pass

    def download_file(self, filename):
        """Download file from blob storage"""
        blob_client = self.container_client.get_blob_client(filename)
        file_blob = blob_client.download_blob().readall()
        self.mediator.notify(self, "P", None)
        return file_blob

    def delete(self, filename):
        pass

    def list_blobs(self):
        print("\nListing blobs...")
        blobs = []
        # List the blobs in the container
        blob_list = self.container_client.list_blobs()
        blobs = [blob.name for blob in blob_list]
        print(blobs)
        return blobs

    def find_blob(self, filename):
        return filename in self.blob_list


def save_file_for_processing(blob, filepath):  # it save the logo and scad file on PROCESSING_DIRECTORY
    with open(filepath, "wb") as file:
        file.write(blob)


# blob_file_obj = AzureBlobFileService()
# blob_logo_obj = AzureBlobLogoService()
# absolute_path = os.path.dirname(__file__)
# relative_file_path = "../ProcessingService/PROCESSING_DIRECTORY/keychain.scad"
# relative_logo_path = "../ProcessingService/PROCESSING_DIRECTORY/azure.svg"
# save_file_for_processing(blob_file_obj.download_file("keychain.scad"), relative_file_path)
# save_file_for_processing(blob_logo_obj.download_file("azure.svg"), relative_file_path)
