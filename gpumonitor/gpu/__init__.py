import random
import subprocess
from abc import ABCMeta, abstractmethod
from typing import Optional, List

from .gpuinfo import GPUInfo


class IGPUSystemManagementWrapper(metaclass=ABCMeta):
    @abstractmethod
    def poll_data(self) -> Optional[List[GPUInfo]]:
        raise NotImplementedError


class NvidiaSMIWrapper(IGPUSystemManagementWrapper):
    __gpu_status_cols__ = [
        'index',
        'name',
        'timestamp',
        'driver_version',
        'temperature.gpu',
        'utilization.gpu',
        'memory.used',
        'memory.total',
        'fan.speed',
        'power.draw',
        'power.limit'
    ]

    def __init__(self):
        self._smi_process_out = None
        self._smi_process_err = None

    def _invoke_smi(self):
        smi_process = subprocess.Popen(
            [
                'nvidia-smi',
                f'--query-gpu={",".join(NvidiaSMIWrapper.__gpu_status_cols__)}',
                '--format=csv,nounits'
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        self._smi_process_out, self._smi_process_err = smi_process.communicate()

    def _process_smi_out(self) -> Optional[List[GPUInfo]]:
        if not self._smi_process_out:
            raise TypeError('Invalid process output')

        results = self._smi_process_out.decode().strip().split('\r\n')
        columns = results.pop(0)
        columns = [col.strip() for col in columns.split(',')]

        if len(columns) != len(NvidiaSMIWrapper.__gpu_status_cols__):
            raise OSError('Process failed')

        if len(results) == 0:
            raise ValueError('Insufficient process output')

        gpu_info_list = list()
        for entry in results:
            gpu_info = GPUInfo()

            for k, v in zip(columns, [val.strip() for val in entry.split(',')]):
                gpu_info[k] = v

            gpu_info_list.append(gpu_info)

        return gpu_info_list

    def poll_data(self) -> Optional[List[GPUInfo]]:

        try:
            self._invoke_smi()
        except TimeoutError:
            print('[ERROR] Output timeout')
            print('nvidia-smi is not responding properly')
            return
        except OSError:
            print('[ERROR] Unable to call nvidia-smi')
            print(
                'Please check whether nvidia-smi program is installed properly or accessible via environment variables')
            return
        except Exception as e:
            print('[ERROR]', e)
            return

        try:
            gpu_info_list = self._process_smi_out()
        except ValueError:
            print('[ERROR] No GPU found')
            print('Please check whether GPU is/are working properly')
            return
        except OSError:
            print('[ERROR] Illegal query column(s)')
            return
        except TypeError as e:
            print('[ERROR]', e)
            return

        return gpu_info_list


class DummySMIWrapper(IGPUSystemManagementWrapper):
    def __init__(self):
        self._gpu_1 = GPUInfo({
            'idx': 0,
            'name': 'GeForce GTX 1070 Ti',
            'timestamp': '2020/07/19 19:31:56.313',
            'driver_version': '451.48',
            'temp': 42,
            'util': 45,
            'mem used': 2231,
            'mem available': 8192,
            'fan speed': 38,
            'power usage': 43.08,
            'power cap': 180.00
        })

        self._counter = 0

        self._gpu_2 = GPUInfo({
            'idx': 1,
            'name': 'GeForce GTX 1080 Ti',
            'timestamp': '2020/07/19 19:31:56.313',
            'driver_version': '451.48',
            'temp': 42,
            'util': 45,
            'mem used': 2231,
            'mem available': 16384,
            'fan speed': 38,
            'power usage': 43.08,
            'power cap': 180.00
        })

    @staticmethod
    def _rnd():
        return random.randint(-5, 5)

    def poll_data(self) -> Optional[List[GPUInfo]]:
        rnd = DummySMIWrapper._rnd

        self._gpu_1['temp'] = self._counter + rnd()
        self._gpu_2['temp'] = 105 - self._counter + rnd()

        self._gpu_1['util'] = self._counter + rnd()
        self._gpu_2['util'] = 105 - self._counter + rnd()

        self._gpu_1['mem used'] = int(8192 * self._counter / 100) + rnd()
        self._gpu_2['mem used'] = int(16384 * (1 - self._counter / 100)) + rnd()

        self._gpu_1['fan speed'] = self._counter + rnd()
        self._gpu_2['fan speed'] = 105 - self._counter + rnd()

        self._gpu_1['power usage'] = round(180.0 * self._counter / 100 + rnd(), 2)
        self._gpu_2['power usage'] = round(180.0 * (1 - self._counter / 100) + rnd(), 2)

        self._counter = (self._counter + 5) % 106

        return [self._gpu_1, self._gpu_2]


__all__ = [
    IGPUSystemManagementWrapper,
    NvidiaSMIWrapper,
    DummySMIWrapper
]
