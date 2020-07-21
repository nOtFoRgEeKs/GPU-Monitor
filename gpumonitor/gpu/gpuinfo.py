class GPUInfo(dict):
    __attr__ = {
        'index': ('idx', int),
        'temperature.gpu': ('temp', int),
        'utilization.gpu [%]': ('util', int),
        'memory.used [MiB]': ('mem used', int),
        'memory.total [MiB]': ('mem available', int),
        'fan.speed [%]': ('fan speed', int),
        'power.draw [W]': ('power usage', float),
        'power.limit [W]': ('power cap', float)
    }

    def __setitem__(self, key, val):
        key, val = (GPUInfo.__attr__[key][0], GPUInfo.__attr__[key][1](val)) if key in GPUInfo.__attr__ else (key, val)
        super().__setitem__(key, val)
