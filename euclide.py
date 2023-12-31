


class factors:

    def __init__(self, num, factor = 1) -> None:
        self.num = num
        self.factor = factor
        if type(num) == factors:
            self.num = num.num
            self.factor = factor * num.factor
        if type(factor) == factors:
            a = self.num if self.num is not None else 1
            b = factor.num if factor.num is not None else 1
            self.num = a*b
            self.factor = self.factor.factor

    def __mul__(self, __value) -> object:
        return factors(self.num, __value * self.factor)
    
    def __add__(self, __value) -> object:
        if type(__value) == int or type(__value) == factors:
            __value = factors(__value)
            if self.num == __value.num:
                return factors(self.num, self.factor + __value.factor)
            return pair(self, -__value)
        return NotImplemented
    
    def __radd__(self, __value) -> object:
        return self + __value
    
    def __sub__(self, __value) -> object:
        return self + __value*-1
    
    def __rsub__(self, __value) -> object:
        return -self + __value

    def __neg__(self) -> object:
        return self * -1
    
    def __str__(self) -> str:
        return '{}({})'.format(self.num if self.num != None else 1, self.factor)
    
    def __repr__(self) -> str:
        return 'factors[ {} ]'.format(str(self))
    
    @property
    def value(self) -> int:
        return self.num * self.factor if self.num is not None else self.factor

class pair:

    def __init__(self, fs) -> None:
        if type(fs) == dict:
            self.fs = fs
        elif type(fs) == list or type(fs) == tuple:
            self.fs = {}
            for n in fs:
                f = factors(n)
                self._add_factor(self.fs, f)
    
    def __mul__(self, __value) -> object:
        if type(__value) == int:
            new_fs = self.fs.copy()
            for key in new_fs:
                new_fs[key] *= __value
            return pair(new_fs)
    
    def __add__(self, __value) -> object:
        new_fs = self.fs.copy()
        if type(__value) == int or type(__value) == factors:
            __value = factors(__value)
            self._add_factor(new_fs, __value)
            return pair(new_fs)
        elif type(__value) == pair:
            new_pair = pair(self.fs)
            for num in __value.fs:
                new_pair = new_pair + factors(num, __value.fs[num])
            return new_pair
    
    def _add_factor(self, fs:dict, f:factors):
        if f.num in fs:
            fs[f.num] += f.factor
        else:
            fs[f.num] = f.factor

    def __radd__(self, __value) -> object:
        return self + __value
    
    def __sub__(self, __value) -> object:
        return self + (__value*-1)
    
    def __rsub__(self, __value) -> object:
        return -self + __value
    
    def __neg__(self) -> object:
        return self * -1
    
    def __str__(self) -> str:
        string = ''
        for num in self.fs:
            string += '{}({}) + '.format(num, self.fs[num])
        return string[:-3]
    
    def __repr__(self) -> str:
        return 'pair[ {} = {} ]'.format(self.value, str(self))
    
    def rotate(self) -> object:
        return pair(-self.f2, -self.f1)
    
    @property
    def value(self) -> int:
        gcd = 0
        for num in self.fs:
            gcd += num * self.fs[num]
        return gcd
    
def bezout_id(k, n):
    if k == 0:
        return pair((factors(k, 0), n))
    r0 = pair((k, factors(n, 0)))
    r1 = n - r0 * (n//r0.value)
    while(r1.value != 0):
        r2 = r0 - r1 * (r0.value//r1.value)
        r0, r1 = r1, r2
    return r0

def optimal_t(j, k, n):
    eq = bezout_id(k % n, n)
    j = j % n
    if j % eq.value != 0:
        return -1, eq.value   # doesn't exist
    return eq.f1.factor * (j//eq.value) % (n//eq.value), k * n // eq.value  # t, lcm

def lcm(args):
    lcm = 1
    for n in args:
        lcm = n * lcm // bezout_id(n, lcm).value
    return lcm