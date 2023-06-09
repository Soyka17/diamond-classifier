import os
from dataclasses import dataclass


@dataclass
class ConfigData:
    file: str                                   # Test data file
    spectrum: str                               # Spectrum of stone


def get_from_env() -> ConfigData:
    file = os.getenv('FILE')
    spectrum = os.getenv('SPECTRUM')

    return ConfigData(
        file=file,
        spectrum=spectrum
    )
