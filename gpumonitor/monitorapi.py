import time

from gpumonitor.gpu import DummySMIWrapper, NvidiaSMIWrapper
from gpumonitor.output import TabularOutput


# import os


class MonitorAPI:
    def __init__(self, debug=False):
        self._smi_wrapper = DummySMIWrapper() if debug else NvidiaSMIWrapper()
        self._output_handler = TabularOutput()

    @property
    def gpu_information(self):
        return self._smi_wrapper.poll_data()

    def start(self, delay=1):
        # os.system('cls')
        try:
            while True:
                self._output_handler.flush()

                gpu_info_list = self._smi_wrapper.poll_data()

                if not gpu_info_list:
                    break
                self._output_handler.print(gpu_info_list)

                time.sleep(delay)
        except KeyboardInterrupt:
            # os.system('cls')
            self._output_handler.flush()
        finally:
            return


def main(*argv):
    api = MonitorAPI(debug=True)

    api.start()
