from dia.config import config_reader
from dia.parsers import parsers
from dia.classifier import classifier
import logging


def __close(msg, is_error):
    if is_error:
        logging.error(msg)
    else:
        logging.info(msg)
    exit()


def main():
    config_data = config_reader.get_from_env()
    if not config_data.is_cli:
        logging.basicConfig(
            format="%(levelname)-8s [%(asctime)s] %(message)s",
            level="INFO"
        )
        logging.info("Classifier start")

    if config_data.is_cli:
        file = input("Input path to file:")
    else:
        if config_data.file is None:
            __close("Path to file is required", True)
        file = config_data.file

    try:
        data = parsers.parse_lines(file)
    except FileNotFoundError:
        __close("File not found", True)

    classifiers = classifier.get_classifiers()

    if config_data.is_cli:
        spectrum = input("Input spectrum:")
    else:
        if config_data.spectrum not in classifiers.keys():
            __close("Incorrect spectrum specified", True)
        spectrum = config_data.spectrum

    result = classifiers[spectrum](data)

    res_str = ""
    for i in result:
        res_str += f"{i}={result[i]}  "

    if config_data.is_cli:
        print(res_str)
    else:
        logging.info(res_str)

    __close("Classifier shutdown", False)


if __name__ == "__main__":
    main()
