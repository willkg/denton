def eq_(a, b, msg=None):
    if msg is None:
        msg = '{0} != {1}'.format(repr(a), repr(b))
    assert a == b, msg


def raises_(exc, fun, msg=None):
    if msg is None:
        msg = 'Did not raise {0}'.format(exc)
    try:
        fun()
    except Exception as raised_exc:
        assert isinstance(raised_exc, exc), msg
