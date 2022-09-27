import os
import pathlib
from openscad_runner import OpenScadRunner

from ServiceController.service_controller import ServiceBaseController

current_path = pathlib.Path(__file__).parent.resolve()
current_directory = os.getcwd()
logos = ["", "azure.svg", "hashicorp.svg", "terraform.svg", "tp_bw.svg"]


class ProcessingServiceBase(ServiceBaseController):

    def __init__(self, name=None, logo=None):
        self.name = name
        self.logo = logo

    def replace_scad_setting(self):
        if len(self.name) != 0:
            # input file
            fin = open("ProcessingService/PROCESSING_DIRECTORY/keychain.scad", "rt")
            # output file to write the result to
            fout = open("ProcessingService/PROCESSING_DIRECTORY/keychain_out.scad", "wt")
            # for each line in the input file
            for line in fin:
                # read replace the string and write to output file
                line_adusted = line.replace("Sometext", self.name).replace("Somelogo", self.logo)
                fout.write(line_adusted)
            # close input and output files
            fin.close()
            fout.close()

    # def convert_scad_stl(self):
    #     os.system(f"docker run -v $(pwd):/openscad openscad/openscad:2021.01 openscad "
    #               f"PROCESSING_DIRECTORY/keychain_out.scad -o "
    #               f"PROCESSING_DIRECTORY/keychain.stl")
    #     os.remove("PROCESSING_DIRECTORY/keychain_out.scad")

    def scad_stl_converter(self, scad_filepath, stl_filepath):
        # os.remove("PROCESSING_DIRECTORY/keychain.stl")
        self.replace_scad_setting()
        osr = OpenScadRunner(scad_filepath, stl_filepath)
        osr.run()
        for line in osr.echos:
            print(line)
        for line in osr.warnings:
            print(line)
        for line in osr.errors:
            print(line)
        if osr.good():
            print("Successfully created keychain.stl")
            os.remove("ProcessingService/PROCESSING_DIRECTORY/keychain.scad")
            os.remove("ProcessingService/PROCESSING_DIRECTORY/keychain_out.scad")
            self.mediator.notify(self, "E", None)


# processing = ProcessingServiceBase("Max", logos[2])
# processing.replace_scad_setting()
# scad_filepath = "PROCESSING_DIRECTORY/keychain_out.scad"
# stl_filepath = "PROCESSING_DIRECTORY/keychain.stl"
# processing.scad_stl_converter(scad_filepath, stl_filepath)
# processing.convert_scad_stl()
