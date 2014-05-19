import textwrap
import unittest

from denton import utils

from . import eq_, raises_


class TestDT(unittest.TestCase):
    dt = utils.DenTemplate()

    def test_parsing(self):
        eq_(self.dt.templatize('foo {{ bar.get("blue", {})["bar"] }} baz', {}),
            'foo UNDEFINED baz')

    def test_eval(self):
        eq_(self.dt.templatize('{{ foo }}', {'foo': 'a'}), 'a')
        eq_(self.dt.templatize('{{ foo }}', {'foo': 1}), '1')
        raises_(NameError, lambda: self.dt.templatize('{{ foo }}', {}))

    def test_missing_eval(self):
        eq_(self.dt.templatize('{{ foo }}', {}), 'UNDEFINED')
        eq_(self.dt.templatize('{{ foo["bar"] }}', {}), 'UNDEFINED')

    def test_if(self):
        template = textwrap.dedent("""\
        {% if True %}
        True
        {% endif %}""")

        eq_(self.dt.templatize(template, {}), 'True')

        template = textwrap.dedent("""\
        {% if True %}
        True
        {% else %}
        False
        {% endif %}""")

        eq_(self.dt.templatize(template, {}), 'True')

        template = textwrap.dedent("""\
        {% if False %}
        True
        {% else %}
        False
        {% endif %}""")

        eq_(self.dt.templatize(template, {}), 'False')

        template = textwrap.dedent("""\
        {% if len(resps) == 3 %}
        True
        {% else %}
        False
        {% endif %}""")

        eq_(self.dt.templatize(template, {'resps': [1, 2, 3]}), 'True')

    def test_for(self):
        template = textwrap.dedent("""\
        {% for mem in range(5) %}
        {{ mem }}
        {% endfor %}""")

        eq_(self.dt.templatize(template, {}),
            '01234')

        template = textwrap.dedent("""\
        {% for mem in range(5) %}
        {{ mem }}

        {% endfor %}""")

        eq_(self.dt.templatize(template, {}),
            '0\n1\n2\n3\n4\n')

    def test_complex(self):
        template = textwrap.dedent("""\
        {% if resps %}
        {% for resp in resps %}
        {{ resp['name'] }}

        {% endfor %}
        {% else %}
        You didn't do squat.
        {% endif %}""")

        eq_(self.dt.templatize(template, {'resps': []}),
            'You didn\'t do squat.')

        eq_(self.dt.templatize(template, {'resps': [{'name': 'joe'}]}),
            'joe\n')
