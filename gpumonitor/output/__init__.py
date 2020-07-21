import math
from abc import ABCMeta, abstractmethod
from typing import List

from gpumonitor.common import constants
from gpumonitor.gpu import GPUInfo
from gpumonitor.common.colors import *
from .helper import ConsolePrinter

a_l = ConsolePrinter.add_line
s_w = ConsolePrinter.show_window
f_w = ConsolePrinter.flush_window


class IOutputHandler(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def print(gpu_info_list: List[GPUInfo]):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def flush():
        raise NotImplementedError


class TabularOutput(IOutputHandler):
    _WINDOW_WIDTH = 100
    _PADDING_WIDTH = 1
    _PADDING = ' ' * _PADDING_WIDTH
    _BORDER_WIDTH = 1

    @staticmethod
    def flush():
        f_w()

    @staticmethod
    def print(gpu_info_list: List[GPUInfo]):
        tool_name = constants.name
        window_width = TabularOutput._WINDOW_WIDTH
        padding_width = TabularOutput._PADDING_WIDTH
        padding = TabularOutput._PADDING
        border_width = TabularOutput._BORDER_WIDTH

        timestamp = gpu_info_list[0]['timestamp']
        driver_ver = gpu_info_list[0]['driver_version']

        # SECTION: Header
        left_cell_width = window_width // 2 - border_width
        right_cell_width = window_width - left_cell_width - padding_width - border_width

        a_l('+', '-' * (window_width - 2 * border_width), '+')
        a_l('|', TITLE, f'{padding}{tool_name}'.ljust(left_cell_width),
            f'{timestamp}{padding}'.rjust(right_cell_width), FORMAT_OFF, '|')
        a_l('|', TITLE,
            f'{padding}NVIDIA-SMI  Driver Version: {driver_ver}'.ljust(window_width - 2 * border_width),
            FORMAT_OFF, '|')
        a_l('+', '-' * (window_width - 2 * border_width), '+')

        a_l()

        left_cell_width = window_width * 3 // 11 - 2 * border_width
        right_cell_width = window_width - left_cell_width - 3 * border_width

        right_cell_label = right_cell_width * 2 // 9
        right_cell_bar = right_cell_width * 11 // 20
        right_cell_status = right_cell_width - right_cell_label - right_cell_bar

        a_l('+', '-' * left_cell_width, '+', '-' * right_cell_width, '+')

        for gpu_info in gpu_info_list:
            index = gpu_info['idx']
            name = gpu_info['name']
            temp_color, temp = TabularOutput._format_temp(gpu_info['temp'])
            util = gpu_info['util']
            mem_used = gpu_info['mem used']
            mem_total = gpu_info['mem available']
            fan_speed = gpu_info['fan speed']
            pow_used = gpu_info['power usage']
            pow_cap = gpu_info['power cap']

            a_l('|', DEVICE_INFO, f'{padding}Device {index}'.ljust(left_cell_width), FORMAT_OFF, '|',
                LABEL, f'Temperature{padding}'.rjust(right_cell_label), FORMAT_OFF,
                ' ' * right_cell_bar,
                temp_color, f'{temp}{padding}'.rjust(right_cell_status), FORMAT_OFF, '|')

            a_l('|', DEVICE_INFO, f'{padding}{name}'.ljust(left_cell_width), FORMAT_OFF, '|',
                LABEL, f'Mem. usage{padding}'.rjust(right_cell_label), FORMAT_OFF,
                f'{padding}{TabularOutput._generate_graph(right_cell_bar - 2 * padding_width, mem_used, mem_total)}{padding}',
                STATUS, f'{mem_used} / {mem_total} MB{padding}'.rjust(right_cell_status), FORMAT_OFF, '|')

            a_l('|', ' ' * left_cell_width, '|',
                LABEL, f'GPU usage{padding}'.rjust(right_cell_label), FORMAT_OFF,
                f'{padding}{TabularOutput._generate_graph(right_cell_bar - 2 * padding_width, util)}{padding}',
                STATUS, f'{util} %{padding}'.rjust(right_cell_status), FORMAT_OFF, '|')

            a_l('|', ' ' * left_cell_width, '|',
                LABEL, f'Fan speed{padding}'.rjust(right_cell_label), FORMAT_OFF,
                f'{padding}{TabularOutput._generate_graph(right_cell_bar - 2 * padding_width, fan_speed)}{padding}',
                STATUS, f'{fan_speed} %{padding}'.rjust(right_cell_status), FORMAT_OFF, '|')

            a_l('|', ' ' * left_cell_width, '|',
                LABEL, f'Power usage{padding}'.rjust(right_cell_label), FORMAT_OFF,
                f'{padding}{TabularOutput._generate_graph(right_cell_bar - 2 * padding_width, pow_used, pow_cap)}{padding}',
                STATUS, f'{pow_used} / {int(pow_cap)} W{padding}'.rjust(right_cell_status), FORMAT_OFF, '|')

            a_l('+', '-' * left_cell_width, '+', '-' * right_cell_width, '+')

        s_w()

    @staticmethod
    def _format_temp(temp):

        temp_color = TEMP_OK

        if 60 <= temp < 80:
            temp_color = TEMP_HIGH

        if 80 <= temp:
            temp_color = TEMP_WARN

        return temp_color, f'{temp} C'

    @staticmethod
    def _generate_graph(width, val, max_val=100, ch='='):
        graph = '['

        ratio = val / max_val

        if ratio < 0.2:
            graph_color = GRAPH_LOW
        elif 0.2 <= ratio < 0.5:
            graph_color = GRAPH_MEDIUM
        elif 0.5 <= ratio < 0.7:
            graph_color = GRAPH_MEDIUM_HIGH
        elif 0.7 <= ratio < 0.9:
            graph_color = GRAPH_HIGH
        else:
            graph_color = GRAPH_WARN
        graph += graph_color

        graph_len = math.ceil((width - 2) * ratio) if ratio < 1 else (width - 2)
        graph += ch * graph_len
        graph += FORMAT_OFF
        graph += ' ' * (width - 2 - graph_len)
        graph += ']'

        return graph
