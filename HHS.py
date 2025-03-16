class HHS:
    def __init__(self):
        self.env = {}

    def let(self, var, value):
        self.env[var] = value

    def print_(self, *args):
        output = []
        for arg in args:
            if isinstance(arg, str) and arg in self.env:  
                output.append(self.env[arg])
            else:
                output.append(arg)
        print(*output)

    def if_(self, condition, then_block, else_block=None):
        if condition():
            then_block()
        elif else_block:
            else_block()

    def while_(self, condition, loop_block):
        while condition():
            loop_block()

    def def_(self, name, func):
        self.env[name] = func

    def add(self, a, b): return self._get_value(a) + self._get_value(b)
    def sub(self, a, b): return self._get_value(a) - self._get_value(b)
    def mul(self, a, b): return self._get_value(a) * self._get_value(b)
    def div(self, a, b): return self._get_value(a) / self._get_value(b) if self._get_value(b) != 0 else "[錯誤] 除數不能為 0"
    def mod(self, a, b): return self._get_value(a) % self._get_value(b) if self._get_value(b) != 0 else "[錯誤] 除數不能為 0"

    def and_(self, a, b): return self._get_value(a) and self._get_value(b)
    def or_(self, a, b): return self._get_value(a) or self._get_value(b)
    def not_(self, a): return not self._get_value(a)

    def _get_value(self, var):
        return self.env[var] if isinstance(var, str) and var in self.env else var

if __name__ == '__main__':
    hhs = HHS()

    hhs.let("a", 10)
    hhs.let("b", 5)
    hhs.let("x", True)
    hhs.let("y", False)

    hhs.print_("a + b =", hhs.add("a", "b"))
    hhs.print_("a - b =", hhs.sub("a", "b"))
    hhs.print_("a * b =", hhs.mul("a", "b"))
    hhs.print_("a / b =", hhs.div("a", "b"))
    hhs.print_("a % b =", hhs.mod("a", "b"))

    hhs.print_("x AND y =", hhs.and_("x", "y"))
    hhs.print_("x OR y =", hhs.or_("x", "y"))
    hhs.print_("NOT x =", hhs.not_("x"))