"""

Este metodo eh muito mais simples que o outro. Eu prefiro este, que
funciona bem para os dois exemplos, mas não para a parte 1... estranho.

"""
# %%
from abc import abstractmethod
from collections import OrderedDict

# %%


class Module:
    """Modules communicate using pulses. Each pulse is either a high
    pulse or a low pulse. When a module sends a pulse, it sends that
    type of pulse to each module in its list of destination modules.

    Pulses are always processed in the order they are sent. So, if a
    pulse is sent to modules a, b, and c, and then module a processes
    its pulse and sends more pulses, the pulses sent to modules b and c
    would have to be handled first.

    Design: pulses are transmitted in 2 stages. In the first stage,
    self.output_signal is put to every output_module's input_stack,
    this is done by calling self.send(). In the second stage, each
    module processes its input_stack, and updates its own
    output_signal, this is done by calling self.tick().
    """

    def __init__(self, name):
        self.name = name
        self.input_modules = None
        self.output_modules = None

        # stack of signals received from input modules
        # can be None, True, or False
        # low pulse is True, high pulse is False
        # Note that stack behaves differently for each module
        self.input_stack = OrderedDict()

        # signal to be sent to output modules in each tick
        self.output_signal = None

        # counter for low and high pulses sent
        self.counter = [0, 0]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

    def set_input_modules(self, input_modules):
        self.input_modules = input_modules

    def set_output_modules(self, output_modules):
        self.output_modules = output_modules

    def send(self):
        # send output signal to output modules' stacks
        if self.output_signal is None:
            return
        for out in self.output_modules:
            if VERBOSE:
                print(f"{self.name} sent {self.output_signal} to {out.name}")
            self.counter[0 if self.output_signal else 1] += 1
            out.put(self.output_signal, self)

    def put(self, signal, sender):
        # put signal to own's input stack
        if VERBOSE:
            print(f"{self.name} received {signal} from {sender.name}")
        self.input_stack[sender] = signal

    @abstractmethod
    def tick(self):
        # process own input stack and update output signal
        # return True is a signal is processed, False otherwise
        raise NotImplementedError


class Dummy(Module):
    """A dummy module that does nothing.

    In Part2, this is the output module rx, which counts the number of
    low pulses it receives. It has no output modules.

    """

    def __init__(self, name):
        super().__init__(name)
        self.count_low_pulses = 0

    def send(self):
        pass

    def put(self, signal, sender):
        if VERBOSE:
            print(f"{self.name} received {signal} from {sender.name}")
        if signal:
            self.count_low_pulses += 1

    def tick(self):
        return False


class Broadcaster(Module):
    """Model for both Broadcaster and Button modules.

    There is a single broadcast module (named broadcaster).
    When it receives a pulse, it sends the same pulse to all of
    its destination modules.

    A module with a single button on it called the button module.
    When you push the button, a single low pulse is sent directly to
    the broadcaster module.
    """

    def __init__(self, name):
        super().__init__(name)

    def tick(self):
        # broadcaster and button only send low pulses
        if not self.input_stack:
            self.output_signal = None
            return False
        sender, signal = self.input_stack.popitem(last=False)
        self.output_signal = signal
        return True


class FlipFlop(Module):
    """Flip-flop modules (prefix %) are either on or off; they are
    initially off. If a flip-flop module receives a high pulse, it is
    ignored and nothing happens. However, if a flip-flop module
    receives a low pulse, it flips between on and off. If it was off,
    it turns on and sends a high pulse. If it was on, it turns off and
    sends a low pulse.
    """

    def __init__(self, name):
        super().__init__(name)

        # module state, can be "on" or "off"
        self.state = "off"

    def tick(self):
        if not self.input_stack:
            self.output_signal = None
            return False
        sender, signal = self.input_stack.popitem(last=False)
        if not signal:  # ignore high pulses and None pulses
            self.output_signal = None
        elif self.state == "off":
            self.state = "on"
            self.output_signal = False
        else:
            self.state = "off"
            self.output_signal = True
        return True


class Conjunction(Module):
    """Conjunction modules (prefix &) remember the type of the most
    recent pulse received from each of their connected input modules;
    they initially default to remembering a low pulse for each input.
    When a pulse is received, the conjunction module first updates its
    memory for that input. Then, if it remembers high pulses for all
    inputs, it sends a low pulse; otherwise, it sends a high pulse.

    Here stack needs to know where the pulse is coming from, and we
    also need a memory for the most recent pulse received from each
    input module, so stack is converted into a dictionary, with keys
    being the input modules and values being the most recent pulses.
    """

    def __init__(self, name):
        super().__init__(name)
        self.stack_memory = None

    def set_input_modules(self, input_modules):
        self.input_modules = input_modules
        # initialize memory with default low signal
        self.stack_memory = {mod: True for mod in input_modules}

    def put(self, signal, sender):
        # put signal to own's input stack
        if VERBOSE:
            print(f"{self.name} received {signal} from {sender.name}")
        self.stack_memory[sender] = signal
        self.input_stack[sender] = signal

    def tick(self):
        if not self.input_stack:
            self.output_signal = None
            return False
        self.output_signal = not any(self.stack_memory.values())
        self.input_stack.popitem(last=False)
        return True


def parse_input(data):
    modules = {"button": Broadcaster("button")}
    out_modules_names = {"button": ["broadcaster"]}
    lines = data.strip().splitlines()
    for line in lines:
        typed_name, out_modules_names_i = line.split(" -> ")
        if typed_name == "broadcaster":
            Cls = Broadcaster
            name = "broadcaster"
        elif typed_name.startswith("%"):
            Cls = FlipFlop
            name = typed_name[1:]
        elif typed_name.startswith("&"):
            Cls = Conjunction
            name = typed_name[1:]
        else:
            raise ValueError(f"Unknown module type {typed_name}")

        modules[name] = Cls(name)
        out_modules_names[name] = out_modules_names_i.split(", ")

    # add any missing modules, ie, present only in output modules
    dummy_modules_names = []
    for name in out_modules_names:
        for out_name in out_modules_names[name]:
            if out_name not in modules:
                dummy_modules_names.append(out_name)
    assert len(dummy_modules_names) <= 1, f"There must be one or less dummy modules."
    if dummy_modules_names:
        dummy_name = dummy_modules_names[0]
        modules[dummy_name] = Dummy(dummy_name)
        out_modules_names[dummy_name] = []

    # set output modules
    for name in modules:
        module = modules[name]
        out_modules = []
        for out_name in out_modules_names[name]:
            out_modules.append(modules[out_name])
        module.set_output_modules(out_modules)

    # set input modules
    in_modules = {}
    for name in modules:
        module = modules[name]
        for out_name in out_modules_names[name]:
            if out_name not in in_modules:
                in_modules[out_name] = []
            in_modules[out_name].append(module)
    for name, in_modules in in_modules.items():
        modules[name].set_input_modules(in_modules)

    return modules


# %%


def tick_all(modules):
    """Tick all modules, ie, prepares output signals.
    Return True if any module has a signal to send.
    """
    return any([m.tick() for m in modules.values()])


def send_all(modules):
    """Send all pending signals."""
    [m.send() for m in modules.values()]


def count_pulses(modules):
    low, high = [0, 0]
    for module in modules.values():
        low += module.counter[0]
        high += module.counter[1]
    return low, high


def check_state(modules):
    """Return True is all modules have returned to their initial state,
    ie, all Conjunction modules memories are True, and all FlipFlop
    modules are off.
    """
    # initial_state = True
    # print("  Modules' states:")
    for mod in modules.values():
        if isinstance(mod, Conjunction):
            # print(f"\t{mod.name} memory: {mod.stack_memory.values()}")
            if not all(mod.stack_memory.values()):
                # initial_state = False
                return False
        elif isinstance(mod, FlipFlop):
            # print(f"\t{mod.name} state: {mod.state}")
            if mod.state != "off":
                # initial_state = False
                return False
    # return initial_state
    return True


def click(modules):
    """Push button and tick until all signals are processed."""
    modules["button"].put(True, Dummy(""))
    while tick_all(modules):
        send_all(modules)


def main(data, clicks=1000):
    modules = parse_input(data)

    for _ in range(clicks):
        if VERBOSE:
            print(f"  === Cycle {_ + 1} ===")
        click(modules)
        cycle_period = _ + 1
        if check_state(modules):
            print(f"  Repeated at cycle ", _ + 1)
            break
    else:
        print("  Modules did not return to initial state.")

    cycles = clicks / cycle_period
    assert cycles.is_integer(), f"Cycles must be integer, got {cycles}"
    cycles = int(cycles)
    low, high = [cycles * p for p in count_pulses(modules)]
    print(f"  low: {low}, high: {high}, product: {low * high}")
    return low * high


def example1():
    print("Example 1")
    data = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""
    assert main(data, CLICKS) == 32000000


def example2():
    print("Example 2")
    data = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""
    assert main(data, CLICKS) == 11687500


def part1():
    print("Part 1")
    data = open("day20.txt").read()
    assert main(data, CLICKS) == 879834312


def part2():
    print("Part 2")
    data = open("day20.txt").read()
    main(data, CLICKS, part2=True)


VERBOSE = True
CLICKS = 1000
example1()
example2()
part1()
# part2()

# %%
