from ctypes import *
import subprocess
import sys
import argparse
from parser import memoryParser as mp
from tui import prettyPrint as pprint

def run_iteration(pid, process: subprocess.Popen):
    try:
        mp.attach_ptrace(pid)

        stackStruct = mp.StackStructure()

        regs = mp.init_registers(pid)
        maps = mp.parse_maps(pid)
        stack = mp.locate_stack(maps)

        # Add stack values to stackStruct
        stackStruct.stack_start = mp.convert_void_pointer_addr(stack[0])
        stackStruct.stack_end = mp.convert_void_pointer_addr(stack[1])

        pprint.print_info(f"Stack start: ", f"0x{str(stackStruct.stack_start)}")
        pprint.print_info(f"Stack end: ", f"0x{str(stackStruct.stack_end)}")

        stack_value = mp.ptrace_read_at(pid, c_void_p(regs.rsp))
        stackStruct.add_stack_value(mp.convert_void_pointer_addr(c_void_p(regs.rsp)), stack_value)
        stack_value = mp.ptrace_read_at(pid, c_void_p(c_void_p(regs.rsp).value+8))
        stackStruct.add_stack_value(mp.convert_void_pointer_addr(c_void_p(c_void_p(regs.rsp).value+8)), stack_value)

        stackStruct.print_stack_values()

        pprint.print_info(f"Ptrace continue status: ", f" {mp.ptrace_cont(pid)}", tabs=2)
        pprint.print_success(f"--- Process {pid} completed successfully: ---")

        if process:
            try: 
                print(process.communicate(timeout=5)[0].decode())
            except TimeoutError:
                process.kill()
                print(process.communicate())

    except KeyboardInterrupt:
        pprint.print_error(f"Process with pid {pid} still running, terminating...")
        process.kill()

    # Terminate if we spawned the binary
    # Find different way to kill process if zombie (this terminates too soon.)    
    # Extra safeguard.
    if process:
        process.kill()

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
    
    run_iteration(pid, process)
