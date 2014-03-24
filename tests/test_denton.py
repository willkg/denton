import textwrap
import unittest

from denton import utils

from . import eq_, raises_


class TestDT(unittest.TestCase):
    dt = utils.DenTemplate()

    def test_eval(self):
        eq_(self.dt.templatize('{{ foo }}', {'foo': 'a'}), 'a')
        eq_(self.dt.templatize('{{ foo }}', {'foo': 1}), '1')
        raises_(NameError, lambda: self.dt.templatize('{{ foo }}', {}))

    def test_exec(self):
        eq_(self.dt.templatize('{% print foo %}', {'foo': 'a'}), 'a')
        eq_(self.dt.templatize('{% print foo %}', {'foo': 1}), '1')
        eq_(self.dt.templatize(textwrap.dedent('''\
        {%
        for mem in contents:
            print mem
        %}
        '''), {'contents': ['a', 'b', 'c']}),
            'a\nb\nc')
