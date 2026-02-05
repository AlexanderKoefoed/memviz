from ctypes import *
import subprocess
import sys
import argparse
from parser import memoryParser as mp
from cli_print import prettyPrint as pprint

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="memViz",
        description="Visualize stack and heap memory of running binaries to learn exploitation techniques or debugging attacks!"
    )

    parser.add_argument("-p", "--pid")
    parser.add_argument("-b", "--binary")
    args = parser.parse_args()

    if not len(sys.argv) > 1:
        parser.print_help()
        exit(1)

    pprint.print_welcome()

    if args.pid:
        pid = int(args.pid)
    elif args.binary:
        process = subprocess.Popen([args.binary])
        pid = process.pid

    mp.attach_ptrace(pid)

    regs = mp.init_registers(pid)
    maps = mp.parse_maps(pid)
    stack = mp.locate_stack(maps)

    stackStruct = mp.StackStructure()

    stack_value = mp.ptrace_read_at(pid, c_void_p(regs.rsp))
    stackStruct.add_stack_value(mp.convert_void_pointer_addr(c_void_p(regs.rsp)), stack_value)
    stack_value = mp.ptrace_read_at(pid, c_void_p(c_void_p(regs.rsp).value+8))
    stackStruct.add_stack_value(mp.convert_void_pointer_addr(c_void_p(c_void_p(regs.rsp).value+8)), stack_value)

    stackStruct.print_stack_values()

    # Terminate if we spawned the binary
    if process:
        process.kill()
