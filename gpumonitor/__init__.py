"""
GPU Monitor

A library that monitors NVIDIA GPU activity. It also provides a command-line utility
which prints activity statistics from all the available GPU devices in a tabular form.

[Usage]
API call => Use MonitorAPI to extract GPU activity information in dict format. It also
            provides an api call to print information in stdout in a pretty tabular form.

CLI tool => Directly call 'gpumonitor' in shell to monitor GPU devices

[Note]
1) The MonitorAPI uses NVIDIA System Management Interface utility (nvidia-smi) in the
   backend to collect GPU activity information. Make sure nvidia-smi is installed and working
   properly and accessible via system shell. Otherwise, the api will show error log and exit.

2) Works only with NVIDIA GPUs that are supported by nvidia-smi tool
"""

__version__ = '0.1.0'
__author__ = 'nOtFoRgEeKs'
__email__ = 'aritra8195@gmail.com'
__description__ = 'Library to monitor NVIDIA GPU activity'
__url__ = 'https://github.com'
__license__ = 'GNU GPLv3'

from .monitorapi import MonitorAPI, main

__all__ = [
    __version__,
    __author__,
    __email__,
    __description__,
    __url__,
    __license__,
    MonitorAPI
]
