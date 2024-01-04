from abc import abstractmethod


class Module:
    """Modules communicate using pulses. Each pulse is either a high
    pulse or a low pulse. When a module sends a pulse, it sends that
    type of pulse to each module in its list of destination modules.

    Pulses are always processed in the order they are sent. So, if a
    pulse is sent to modules a, b, and c, and then module a processes
    its pulse and sends more pulses, the pulses sent to modules b and c
    would have to be handled first.
    """

    def __init__(self, name):
        self.name = name
        self.input_modules = None
        self.output_modules = None

        # stack of signals received from input modules
        # can be None, True, or False
        # low pulse is True, high pulse is False
        # Note that stack behaves differently for each module
        self.stack = []

        # counter for low and high pulses sent
        self.counter = [0, 0]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

    def set_input_modules(self, input_modules):
        self.input_modules = input_modules

    def set_output_modules(self, output_modules):
        self.output_modules = output_modules

    @abstractmethod
    def send(self):
        # send signals from own stack to output modules' stack
        raise NotImplementedError

    @abstractmethod
    def receive(self, low_pulse, from_module):
        # receive signals from input modules and save them to a stack
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

    def receive(self, low_pulse, from_module):
        if low_pulse:
            self.count_low_pulses += 1


class Button(Module):
    """A module with a single button on it called the button module.
    When you push the button, a single low pulse is sent directly to
    the broadcaster module.
    """

    def __init__(self, name):
        super().__init__(name)

        # Constant and immutable stack, always send low pulse.
        self.stack = [True]

    def send(self):
        # send a low pulse signal to broadcaster module
        signal = self.stack[0]
        self.counter[0] += 1
        if VERBOSE:
            print(
                f"{self.name} sends {'low' if signal else 'high'} pulse to {self.output_modules[0].name}"
            )
        self.output_modules[0].receive(signal, self)


class Broadcaster(Module):
    """There is a single broadcast module (named broadcaster).
    When it receives a pulse, it sends the same pulse to all of
    its destination modules.
    """

    def __init__(self, name):
        super().__init__(name)

    def send(self):
        # send signals to output modules
        signal = self.stack.pop(0)
        for module in self.output_modules:
            if VERBOSE:
                print(
                    f"{self.name} adds {'low' if signal else 'high'} pulse to {module.name}'s stack"
                )
            module.receive(signal, self)
        for module in self.output_modules:
            if VERBOSE:
                print(
                    f"{self.name} sends {'low' if signal else 'high'} pulse to {module.name}"
                )
            self.counter[0 if signal else 1] += 1
            module.send()

    def receive(self, low_pulse, from_module):
        # receive signals from input modules
        # Broadcaster module only has one input module,
        # so we can just pass the signal to output modules
        assert low_pulse, "Broadcaster module only receives low pulses"
        if VERBOSE:
            print(f"{self.name} receives low pulse from {from_module.name}")
        self.stack.append(low_pulse)
        self.send()


class FlipFlop(Module):
    """Flip-flop modules (prefix %) are either on or off; they are
    initially off. If a flip-flop module receives a high pulse, it is
    ignored and nothing happens. However, if a flip-flop module
    receives a low pulse, it flips between on and off. If it was off,
    it turns on and sends a high pulse. If it was on, it turns off and
    sends a low pulse.

    Here stack will have the length of input modules, and each pulse
    received will be added to the stack, inclusing the Nones.
    """

    def __init__(self, name):
        super().__init__(name)

        # module state, can be "on" or "off"
        self.state = "off"

    def receive(self, low_pulse, from_module):
        if VERBOSE:
            print(
                f"{self.name} receives {'low' if low_pulse else 'high'} pulse from {from_module.name}"
            )
        if not low_pulse:
            send_low_pulse = None
        elif self.state == "off":
            self.state = "on"
            send_low_pulse = False
        else:
            self.state = "off"
            send_low_pulse = True
        self.stack.append(send_low_pulse)

    def send(self):
        signal = self.stack.pop(0)
        if signal is None:
            return
        for module in self.output_modules:
            if VERBOSE:
                print(
                    f"{self.name} adds {'low' if signal else 'high'} pulse to {module.name}'s stack"
                )
            module.receive(signal, self)
        for module in self.output_modules:
            if VERBOSE:
                print(
                    f"{self.name} sends {'low' if signal else 'high'} pulse to {module.name}"
                )
            self.counter[0 if signal else 1] += 1
            module.send()


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

    def update_stack(self):
        assert self.input_modules is not None, "Input modules not set"
        self.stack = {mod: True for mod in self.input_modules}

    def receive(self, low_pulse, from_module):
        if VERBOSE:
            print(
                f"{self.name} receives {'low' if low_pulse else 'high'} pulse from {from_module.name}"
            )
        self.stack[from_module] = low_pulse

    def send(self):
        send_low_signal = not any(self.stack.values())
        for module in self.output_modules:
            if VERBOSE:
                print(
                    f"{self.name} adds {'low' if send_low_signal else 'high'} pulse to {module.name}'s stack"
                )
            module.receive(send_low_signal, self)
        for module in self.output_modules:
            if VERBOSE:
                print(
                    f"{self.name} sends {'low' if send_low_signal else 'high'} pulse to {module.name}"
                )
            self.counter[0 if send_low_signal else 1] += 1
            module.send()


def parse_input(data):
    modules = {"button": Button("button")}
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


def main(data, clicks=1000, part2=False):
    modules = parse_input(data)

    # init conjunction modules
    for module in modules.values():
        if isinstance(module, Conjunction):
            module.update_stack()

    button = modules["button"]
    if part2:
        rx = modules["rx"]
        f = open("day20_rx_pulses.txt", "w")

    for i in range(clicks):
        if part2:
            rx.counter = [0, 0]
        button.send()
        if part2:
            f.write(f"{i}\t{rx.counter[0]}\t{rx.counter[1]}\n")
        # if part2 and rx.counter[0] == 1:
        #     print("rx received a single pulse at i=", i)
        #     exit()

    pulse_counter = [0, 0]
    for module in modules.values():
        pulse_counter = (
            pulse_counter[0] + module.counter[0],
            pulse_counter[1] + module.counter[1],
        )

    print(pulse_counter[0], pulse_counter[1])
    print(pulse_counter[0] * pulse_counter[1])


def example1():
    print("Example 1")
    data = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""
    main(data)


def example2():
    print("Example 2")
    data = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""
    main(data)


def part1():
    print("Part 1")
    data = open("day20.txt").read()
    main(data)


def part2():
    print("Part 2")
    data = open("day20.txt").read()
    main(data, clicks=int(1e9), part2=True)


VERBOSE = False
example1()
example2()
part1()
# part2()
