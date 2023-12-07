from pyaoc2023.day05 import ResourceConverter, Transformer, Range
from rich import print


def test_transformer():
    tr = Transformer.from_data(10, 20, 5)
    rc = ResourceConverter("seed", "soil", (tr,))
    # r = Range(10, 20)
    # print(rc.convert(r))

    # r = Range(20, 25)
    # print(res := rc.convert(r))

    r = Range(15, 25)
    print(r)
    print(tr.transform(r))
    print(res := rc.convert(r))


def test_transformers():
    trs = (
        Transformer.from_data(50, 98, 2),
        Transformer.from_data(52, 50, 48),
    )
    rc = ResourceConverter("seed", "soil", trs)
    print("jeb")
    print(rc.convert(Range(79, 80)))
    print(rc.convert(Range(14, 15)))
    print(rc.convert(Range(55, 56)))
    print(rc.convert(Range(13, 14)))

test_transformer()