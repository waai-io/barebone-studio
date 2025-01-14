import sys
from const import studio_DIRPATH
sys.path.append(studio_DIRPATH)

from studio.api.pickle.pickle_writer import PickleWriter
from studio.api.rules.file_writer import FileWriter
from studio.api.snakemake.snakemake_reader import RuleConfigReader
from studio.routers.model import FILETYPE


if __name__ == '__main__':
    last_output = snakemake.config["last_output"]

    rule_config = RuleConfigReader.read(snakemake.params.name)
    if rule_config.type in [FILETYPE.IMAGE]:
        rule_config.input = snakemake.input
    elif rule_config.type in [FILETYPE.CSV, FILETYPE.BEHAVIOR, FILETYPE.HDF5]:
        rule_config.input = snakemake.input[0]

    rule_config.output = snakemake.output[0]

    if rule_config.type in [FILETYPE.CSV, FILETYPE.BEHAVIOR]:
        outputfile = FileWriter.csv(rule_config, rule_config.type)
        PickleWriter.write(rule_config.output, outputfile)
    elif rule_config.type == FILETYPE.IMAGE:
        outputfile = FileWriter.image(rule_config)
        PickleWriter.write(rule_config.output, outputfile)
    elif rule_config.type == FILETYPE.HDF5:
        outputfile = FileWriter.hdf5(rule_config)
        PickleWriter.write(rule_config.output, outputfile)
