import os
from dataclasses import dataclass


@dataclass
class ConfigData:
    is_cli: bool
    file: str  # Test data file
    spectrum: str  # Spectrum of stone


def get_from_env() -> ConfigData:
    file = os.getenv('FILE')
    spectrum = os.getenv('SPECTRUM')
    is_cli = os.getenv('CLI')
    if is_cli == "false":
        is_cli = False
    else:
        is_cli = True

    return ConfigData(
        file=file,
        spectrum=spectrum,
        is_cli=is_cli
    )
