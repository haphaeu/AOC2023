"""
Another interesting day.

Part 1 is straightforward, handed with some OOP.

Part 2 uses a more complex depth-first search recursive approach.
"""


class Part:
    def __init__(self, x, m, a, s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s
        self.status = None

    def get_xmas(self):
        return self.x, self.m, self.a, self.s

    def __repr__(self):
        return f"Part(x={self.x:4d}, m={self.m:4d}, a={self.a:4d}, s={self.s:4d})"

    def rating(self):
        assert self.status is not None, f"Can't rate part {self.__repr__()}"
        assert (
            self.status in "RA"
        ), f"Invalid status {self.status} for part {self.__repr__()}"
        if self.status == "R":
            return 0
        return self.x + self.m + self.a + self.s


def parse_workflow(wf):
    """Parse a workflow string into a name and a list of rules:

        name, [(condition, next_workflow), ...]
    Eg:
        >> wf = 'qqz{s>2770:qs,m<1801:hdj,R}'
        >> parse_workflow(wf)
        'qqz', [('s>2770', 'qs'), ('m<1801', 'hdj'), 'R']
    """
    name = wf.split("{")[0]
    rules_raw = wf[wf.find("{") + 1 : -1].split(",")
    rules = []
    for i, rule in enumerate(rules_raw):
        if i < len(rules_raw) - 1:
            rule = rule.split(":")
            condition = rule[0]
            next_workflow = rule[1]
            rules.append((condition, next_workflow))
        else:
            next_workflow = rule
            rules.append((next_workflow))
    return name, rules


def parse_workflows(wfs):
    return {name: rules for name, rules in map(parse_workflow, wfs)}


def parse_part(part):
    """Parse a part string into a Part object.

    Eg:
        >> part = '{x=787,m=2655,a=1222,s=2876}'
        >> parse_part(part)
        Part(x=787, m=2655, a=1222, s=2876)
    """
    categories = [int(val.split("=")[1]) for val in part[1:-1].split(",")]
    return Part(*categories)


def parse_parts(parts):
    return list(map(parse_part, parts))


def process(part, workflow=None):
    if workflow is None:
        print(f"{part}: in", end="")
        workflow = workflows["in"]
    for i, rule in enumerate(workflow):
        if i < len(workflow) - 1:
            condition, next_wf_name = rule
        else:
            condition, next_wf_name = None, rule

        if condition is not None:
            x, m, a, s = part.get_xmas()
            satisfied = eval(condition)
            if not satisfied:
                continue
            else:
                break

    print(f" -> {next_wf_name:3s}", end="")
    if next_wf_name in "AR":
        print()
        part.status = next_wf_name
        return
    process(part, workflows[next_wf_name])


# Part 2


class Conditions:
    """Handles a stack of conditions of a series of chained workflows.
    The conditions are added as strings, eg `x>1234` or `m<=5678`.
    When done, ie, reached an `A`, the list of conditions is parsed
    into a dictionary of the form:
        {
            "x": [min, max],
            "m": [min, max],
            "a": [min, max],
            "s": [min, max],
        }
    Such that the total number of combinations can be calculated.
    """

    def __init__(self):
        self.conditions = None
        self.stack = []

    def __repr__(self):
        return f"Conditions({self.conditions})"

    def add(self, condition):
        """condition is a string of the form 'x>1234'"""
        self.stack.append(condition)

    def reverse_last(self):
        last = self.stack[-1]
        if ">=" in last:
            self.stack[-1] = last.replace(">=", "<")
        elif "<=" in last:
            self.stack[-1] = last.replace("<=", ">")
        elif ">" in last:
            self.stack[-1] = last.replace(">", "<=")
        else:
            self.stack[-1] = last.replace("<", ">=")

    def get_copy(self):
        copy = Conditions()
        copy.conditions = None if self.conditions is None else self.conditions.copy()
        copy.stack = self.stack[:]
        return copy

    def parse_all(self):
        # tuples with range of possible values for vars
        # (min, max) inclusive:
        #     x >= min AND
        #     x <= max
        self.conditions = {
            "x": [1, 4000],
            "m": [1, 4000],
            "a": [1, 4000],
            "s": [1, 4000],
        }
        for cond in self.stack:
            var = cond[0]
            eq = cond[1] if "=" not in cond else cond[1:3]
            val = int(cond[2:]) if "=" not in cond else int(cond[3:])
            idx, f = (0, max) if ">" in eq else (1, min)
            o = 0 if "=" in eq else (1 if eq == ">" else -1)
            self.conditions[var][idx] = f(val + o, self.conditions[var][idx])

    def count_combinations(self):
        self.parse_all()
        combs = 1
        for key, (v0, v1) in self.conditions.items():
            if v0 >= v1:
                return 0
            combs *= v1 - v0 + 1
        return combs


def process2(workflow=None, stack=None):
    """Depth-first search of the workflow tree, keeping track of the
    conditions in a stack. When reaching an `A`, the stack is parsed
    and the total number of combinations is calculated.

    Each possible condition of all workflows is considered, ie,
    the condition is both: (a) satisfied, ie, chained into deeper
    workflows, and (b) rejected, ie, reversed passed to the next
    condition in the same workflow.
    """

    if workflow is None:
        # print("in: ", end="")
        workflow = workflows["in"]

    if stack is None:
        stack = Conditions()

    total_combinations = 0
    for i, rule in enumerate(workflow):
        # print(f"{rule=} ", end="")
        if i < len(workflow) - 1:
            condition, next_wf_name = rule
            stack.add(condition)
        else:
            condition, next_wf_name = None, rule

        if next_wf_name in "AR":
            if next_wf_name == "A":
                combs = stack.count_combinations()
                print("Accepted", combs, stack.stack)
                total_combinations += combs
            else:
                print("Rejected")
        else:
            stack_copy = stack.get_copy()
            total_combinations += process2(workflows[next_wf_name], stack_copy)
        stack.reverse_last()

    return total_combinations


data = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}
 \t
{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
""".strip()

data = open("day19.txt").read().strip()

lines = data.splitlines()

workflows, parts = [], []
top = True
for line in lines:
    if not line.strip():
        top = False
        continue
    if top:
        workflows.append(line.strip())
    else:
        parts.append(line.strip())

workflows = parse_workflows(workflows)
parts = parse_parts(parts)
_ = list(map(process, parts))
print(sum([part.rating() for part in parts]))

# Part 2
print(f"{process2():_}")
# example should be 167_409_079_868_000
# answer            126_107_942_006_821
