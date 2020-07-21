class ConsolePrinter:
    _prev_lines_count = 0
    _del_line_str = '\x1b[1A\x1b[2K'
    _curr_lines = list()

    @staticmethod
    def add_line(*objects):
        objects = [str(obj) for obj in objects]
        ConsolePrinter._curr_lines.append(''.join(objects))

    @staticmethod
    def show_window():
        print(*ConsolePrinter._curr_lines, sep='\n')
        ConsolePrinter._prev_lines_count = len(ConsolePrinter._curr_lines)

    @staticmethod
    def flush_window():
        if ConsolePrinter._prev_lines_count > 0:
            print(ConsolePrinter._del_line_str * ConsolePrinter._prev_lines_count, end='')
        ConsolePrinter._curr_lines.clear()
