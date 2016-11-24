import sys
import math
from operator import itemgetter
from functools import partial


def range(start, stop, step=1.):
    """Replacement for built-in range function.

    :param start: Starting value.
    :type start: number
    :param stop: End value.
    :type stop: number
    :param step: Step size.
    :type step: number
    :returns: List of values from `start` to `stop` incremented by `size`.
    :rtype: [float]
    """

    start = float(start)
    stop = float(stop)
    step = float(step)

    result = [start]
    current = start
    while current < stop:
        current += step
        result.append(current)
    return result


# membership functions
def up(a, b, x):
    a = float(a)
    b = float(b)
    x = float(x)
    if x < a:
        return 0.0
    if x < b:
        return (x - a) / (b - a)
    return 1.0


def down(a, b, x):
    return 1. - up(a, b, x)


def tri(a, b, x):
    a = float(a)
    b = float(b)
    m = (a + b) / 2.
    first = (x - a) / (m - a)
    second = (b - x) / (b - m)
    return max(min(first, second), 0.)


def trap(a, b, c, d, x):
    first = (x - a) / (b - a)
    second = (d - x) / (d - c)
    return max(min(first, 1., second), 0.)


# hedges
def hedge(p, mvalue):
    """Generic definition of a function that alters a given membership function
    by intensifying it in the case of *very* of diluting it in the case of
    *somewhat*.  """

    mvalue = float(mvalue)
    if not p:
        return 0.0
    return math.pow(mvalue, p)

very = partial(hedge, 2.)
extermely = partial(hedge, 3.)
somewhat = partial(hedge, 0.5)
slightly = partial(hedge, 1. / 3.)


def fuzziness(domain, func):
    """The fuzziness of a fuzzy subset is the degree to which the values
    of its membership function cluster around 0.5

    >>> fuzziness(range(-10, 30, 1), profitable)
    0.182114

    :param domain: the domain of the function
    :type domain: list
    :param func: membership function
    :type func: function
    :returns: fuzziness value
    :rtype: float
    """
    domain_size = float(len(domain))
    delta = lambda x: x if (x < 0.5) else (1.0 - x)
    result = (2. / domain_size) * sum([delta(func(val)) for val in domain])
    return result


def approximate(fuzz, n, domain):
    hw = fuzz * (max(domain) - min(domain))
    return partial(tri, n - hw, n + hw)

# fuzzy database queries example
companies = [
    ('a', 500, 7), ('b', 600, -9), ('c', 800, 17),
    ('d', 850, 12), ('e', 900, -11), ('f', 1000, 15),
    ('g', 1100, 14), ('h', 1200, 1), ('i', 1300, -2),
    ('j', 1400, -6), ('k', 1500, 12)
]

profit = itemgetter(2)
sales = itemgetter(1)

percentages = map(float, range(-10, 30, 1))
profitable = partial(up, 0., 15.)
high = partial(up, 600., 1150.)

fand = min


def ffilter(predicate, items):
    snd = itemgetter(1)
    return filter(
        lambda x: snd(x) != 0.0,
        map(predicate, items)
    )


def p1(company):
    value = profitable(profit(company))
    return (company, fand(value, 1))


def p2(company):
    a = profitable(profit(company))
    b = high(sales(company))
    return (company, fand(a, b))


def p3(company):
    a = somewhat(profitable(profit(company)))
    b = very(high(sales(company)))
    return (company, fand(a, b))


# shoe example

sizes = range(4, 13, 0.5)

short = partial(down, 1.5, 1.625)
medium = partial(tri, 1.525, 1.775)
tall = partial(tri, 1.675, 1.925)
very_tall = partial(up, 1.825, 1.95)


#small = partial(down, 4., 6.)
def small(size):
    return down(4., 6., size)


#average = partial(tri, 5., 9.)
def average(size):
    return tri(5., 9., size)


#big = partial(tri, 8., 12.)
def big(size):
    return tri(8., 12., size)


#very_big = partial(up, 11., 13.)
def very_big(size):
    return up(11., 13., size)


#fl.near(20, fl.range(0, 40, 1))(17.5)
near = partial(approximate, 0.125)
around = partial(approximate, 0.25)
roughly = partial(approximate, 0.375)


rules = [
    (short, small),
    (medium, average),
    (tall, big),
    (very_tall, very_big)
]


def updated_func(val, func, size):
    first = func(size)
    return (val * first)


def rulebase(height):
    updated = []
    for input_func, output_func in rules:
        val = input_func(height)
        updated.append(
            partial(updated_func, val, output_func)
        )

    rulebase_function = lambda s: sum([r(s) for r in updated])
    return rulebase_function


def centroid(domain, membership_function):
    fdom = map(membership_function, domain)
    first = sum([a * b for (a, b) in zip(domain, fdom)])
    second = sum(fdom)
    return first / second


def shoe_example(h):
    result = centroid(sizes, rulebase(h))
    return result


def centroid_example():
    domain = map(float, range(0, 10))
    membership_function = partial(trap, 2, 3, 6, 9)
    return centroid(domain, membership_function)


def mand(funcs, val):
    return min([func(val) for func in funcs])


def price_example(man_costs=13.25, comp_price=29.99):
    """
    Pricing goods (Cox, 1994).
    The price should be as high as possible to maximize takings but as low as
    possible to maximize sales. We also want to make a healthy profit (100%
    mark-up on the cost price). We also want to consider what the competition
    is charging.

    rule1: our price must be high
    rule2: our price must be low
    rule3: our price must be around twice the manufacturing costs.
    rule4: if the competition price is not very high then our price must be
           around the competition price.
    """

    prices = range(15., 35., 0.5)
    high = partial(up, 15., 35.)
    low = lambda p: 1 - high(p)
    not_very = lambda v: 1 - very(high(v))

    our_price1 = centroid(prices, partial(mand, [high, low]))
    our_price2 = centroid(
        prices,
        partial(mand, [high, low, around(2.0 * man_costs, prices)]),
    )
    our_price3 = centroid(
        prices,
        partial(
            mand, [
                high, low, around(2.0 * man_costs, prices),
                lambda p: not_very(comp_price) * around(comp_price, prices)(p)
            ]
        )
    )

    print our_price1, our_price2, our_price3


if __name__ == '__main__':

    height = float(sys.argv[1])
    size = shoe_example(height)
    print 'For height of %.2f the shoe size is %.2f' % (height, size)
    price_example()
