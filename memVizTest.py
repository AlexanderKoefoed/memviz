from ctypes import *
import os
import argparse
from terminalDraw import draw_stack_box
# Attach to any PID, read the stack and heap to visualize the memory in a teaching friendly way.

parser = argparse.ArgumentParser(
    prog="memViz",
    description="Visualize stack and heap memory of running binaries to better learn exploitation techniques or debugging attacks!"
)

parser.add_argument("-p", "--pid")
args = parser.parse_args()


libc = cdll.LoadLibrary("libc.so.6")

# Setup ptrace with argument types and return type.
ptrace = libc.ptrace
ptrace.argtypes = [c_int, c_int, c_void_p, c_void_p]
ptrace.restype = c_long

# Setup waitpid
waitpid = libc.waitpid
waitpid.argtypes = [c_int, POINTER(c_int), c_int]
waitpid.restype = c_int

# Ptrace constants from sys/ptrace.h
PTRACE_PEEKTEXT = 1
PTRACE_CONT = 7
PTRACE_SINGLESTEP = 9
PTRACE_GETREGS = 12
PTRACE_ATTACH = 16
PTRACE_DETACH = 17
# Figure this out!
WIFSTOPPED = lambda status: (status & 0xFF) != 0

class UserRegsStruct(Structure):
    _fields_ = [
        ("r15", c_uint64), ("r14", c_uint64), ("r13", c_uint64),
        ("r12", c_uint64), ("rbp", c_uint64), ("rbx", c_uint64),
        ("r11", c_uint64), ("r10", c_uint64), ("r9", c_uint64),
        ("r8", c_uint64), ("rax", c_uint64), ("rcx", c_uint64),
        ("rdx", c_uint64), ("rsi", c_uint64), ("rdi", c_uint64),
        ("orig_rax", c_uint64), ("rip", c_uint64), ("cs", c_uint64),
        ("eflags", c_uint64), ("rsp", c_uint64), ("ss", c_uint64),
        ("fs_base", c_uint64), ("gs_base", c_uint64),
        ("ds", c_uint64), ("es", c_uint64), ("fs", c_uint64), ("gs", c_uint64)
    ]


pid = int(args.pid)
if ptrace(PTRACE_ATTACH, pid, 0, 0) < 0:
    raise OSError("ptrace attach failed")

status = c_int(0)
waitpid(pid, byref(status), 0)
while not WIFSTOPPED(status.value):
    waitpid(pid, byref(status), 0)

print("Attached to process")

regs = UserRegsStruct()
regs = UserRegsStruct()
if ptrace(PTRACE_GETREGS, pid, 0, addressof(regs)) < 0:
    raise OSError("ptrace GETREGS failed")
print(f"Instruction pointer:    0x{regs.rip:x}")
print(f"Stack pointer:          0x{regs.rsp:x}")


def parse_maps(pid):
    maps_arr = []
    with open(f"/proc/{pid}/maps") as maps_file:
        for line in maps_file.readlines():
            maps_arr.append(line)
    return maps_arr

def locate_stack(maps_arr: list[str]):
    for memSection in maps_arr:
        if "[stack]" in memSection:
            stack_start = memSection.split(" ")[0].split("-")[0]
            stack_end = memSection.split(" ")[0].split("-")[1]
            print(f"Stack found at: {stack_start}")
            return [c_void_p(int(stack_start, 16)), c_void_p(int(stack_end, 16))]
    return 0

def convert_void_pointer_addr(c_void_p: c_void_p):
    return hex(c_void_p.value)

def ptrace_read_at(pid, addr):
    ret = ptrace(PTRACE_PEEKTEXT, pid, addr, 0)
    if ret != None:
        return hex(ret) 
    return 0

def read_stack_n(pid, start_addr, n_bytes):
    print("Not yet implemented")

# Might not be necessary. We just use the stack pointer to start parsing the stack
maps = parse_maps(pid)
stack = locate_stack(maps)


class StackStructure:
    def __init__(self):
        self.stack_start =  0x00000000
        self.stack_end =    0x00000000
        self.value_array = []

    def add_stack_value(self, addr: str, value: str):
        obj = {"position": addr, "value": value}
        self.value_array.append(obj)

    def print_stack_values(self):
        if len(self.value_array) > 0:
            for obj in self.value_array:
                draw_stack_box(obj["position"], obj["value"])
                # print(f"Value: {obj["value"]} at position: {obj["position"]}")
            return 1
        print("No stack values parsed")
        return 0
    

stackStruct = StackStructure()

stack_value = ptrace_read_at(pid, c_void_p(regs.rsp))
stackStruct.add_stack_value(convert_void_pointer_addr(c_void_p(regs.rsp)), stack_value)
stack_value = ptrace_read_at(pid, c_void_p(c_void_p(regs.rsp).value+8))
stackStruct.add_stack_value(convert_void_pointer_addr(c_void_p(regs.rsp)), stack_value)

stackStruct.print_stack_values()