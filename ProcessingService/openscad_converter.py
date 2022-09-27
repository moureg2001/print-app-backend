from openscad_runner import OpenScadRunner
osr = OpenScadRunner("PROCESSING_DIRECTORY/keychain.scad", "PROCESSING_DIRECTORY/keychain.stl")
osr.run()
for line in osr.echos:
    print(line)
for line in osr.warnings:
    print(line)
for line in osr.errors:
    print(line)
if osr.good():
    print("Successfully created example.stl")
