# MemViz

Simple tool to visualize memory layout in linux ELF binaries. Can be used to teach about binary exploitation or build attack chains!

If you stumble upon this project, feel free to follow along or come with suggestions for features/improvements! 

NB: This project is very new, experimenting phase, expect everything to change.

Also as a challenge to myself, this project will be built without depending on too many external packages. Of course the python standard library is being used, but I am trying to not install anything else to force handling fun topics myself.

## Todo

- Make memviz spawn the process it needs to attach to.
- Create a better API for printing to the terminal
- cmdParser needs to take commands from users.
- Interactive CLI tool. Take commands from users in cmdParser.py.

## Ideas

- Allow for input of a payload which is then used through exploration of memory layout. User give an offset, then the payload is laid out next to actual memory and viewed.
- After confirmation that the payload is lined up correctly, execute it. Might be hard for complex payloads, but cool for intro level buffer overflows.

### user input

- parse stack: Allow for parsing arbitrary amount of stack with a default value
- parse heap: check if heap is init, the allow for arbitrary parse of heap.

