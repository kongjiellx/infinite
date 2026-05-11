# -*-coding: utf-8 -*-
from colorama import Style

def print_stream_and_return_program(stream, field_func, color):
    pos = 0
    print(color)
    for s in stream:
        val = field_func(s)
        print(f"{val[pos:]}", end="", flush=True)
        pos = len(val)
    print(Style.RESET_ALL)
    return s