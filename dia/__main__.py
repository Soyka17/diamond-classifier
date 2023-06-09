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
    logging.basicConfig(
        format="%(levelname)-8s [%(asctime)s] %(message)s",
        level="INFO"
    )
    logging.info("Classifier start")
    config_data = config_reader.get_from_env()

    if config_data.file is None:
        __close("Path to file is required", True)

    try:
        data = parsers.parse_lines(config_data.file)
    except FileNotFoundError:
        __close("File not found", True)

    classifiers = classifier.get_classifiers()

    if config_data.spectrum not in classifiers.keys():
        __close("Incorrect spectrum specified", True)

    result = classifiers[config_data.spectrum](data)

    res_str = ""
    for i in result:
        res_str += f"{i}={result[i]}  "

    logging.info(res_str)

    __close("Classifier shutdown", False)


if __name__ == "__main__":
    main()
