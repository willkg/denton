import cgi
import json
import re
import urllib2


def request_url(url, is_json=False):
    try:
        resp = urllib2.urlopen(url)
    except urllib2.HTTPError as exc:
        print 'Error with {0}'.format(url)
        raise exc

    data = {
        'status_code': resp.getcode(),
        'body': resp.read()
    }

    if is_json:
        data['json'] = json.loads(data['body'])

    return data


class Text(object):
    def __init__(self, text):
        self.text = text

    def eval(self, globalsdict, env):
        return self.text


class EvalExp(object):
    FILTER_RE = re.compile(
        r'^'                              # begin
        r'\s*([A-Za-z0-9_\-]+)\s*'        # filter name
        r'(?:\s*\(\s*([^\)]+)\s*\))?'     # optional args in ()
        r'\s*$'                           # end
    )
    def __init__(self, exp):
        self.exp = exp

    def apply_filter(self, filt, env, ret):
        parts = self.FILTER_RE.match(filt)
        name = parts.group(1)
        args = parts.group(2)
        return env[name + '_filter'](ret, args, env)

    def eval(self, globalsdict, env):
        exp = self.exp.split('|')
        # FIXME: support filters here
        try:
            ret = eval(exp[0], globalsdict, env)
            for filt in exp[1:]:
                ret = self.apply_filter(filt, env, ret)
            return unicode(ret)
        except (AttributeError, NameError, TypeError):
            return u'UNDEFINED'


class Block(object):
    def __init__(self, blockexp, children):
        self.blockexp = blockexp
        self.children = children

    def eval(self, globalsdict, env):
        output = []
        for mem in self.children:
            output.append(str(mem.eval(globalsdict, env)))
        return u''.join(output)

    def nix_cr(self, children):
        # Nix \n from beginning and ending
        if children:
            if children[0][0] == '\n':
                children[0] = children[0][1:]
            if children[-1][-1] == '\n':
                children[-1] = children[-1][:-1]
        return children


class IfBlock(Block):
    IF_RE = re.compile(r'^\s*if\s+(.+)\s*$')
    def eval(self, globalsdict, env):
        parts = self.IF_RE.match(self.blockexp)
        exp = parts.group(1)
        exp = eval(exp, globalsdict, env)
        if not exp:
            return u''

        output = []
        for child in self.children:
            output.append(child.eval(globalsdict, env))

        output = self.nix_cr(output)
        return u''.join(output)


class ForBlock(Block):
    FOR_RE = re.compile(r'^\s*for\s+([\w]+)\s+in\s+(.+)\s*$')
    def eval(self, globalsdict, env):
        parts = self.FOR_RE.match(self.blockexp)
        var_ = parts.group(1)
        iter_ = eval(parts.group(2), globalsdict, env)

        output = []
        for mem in iter_:
            env[var_] = mem

            blockoutput = []
            for child in self.children:
                blockoutput.append(child.eval(globalsdict, env))

            output.extend(self.nix_cr(blockoutput))

        return u''.join(output)


class ParseError(Exception):
    pass


def datetime_filter(value, args, env):
    """Takes a date/datetime and applies strftime to it"""
    # FIXME: This doesn't handle escaped quotes and doesn't
    # handle strings that are dates.
    args = args.strip('"').strip("'")
    return value.strftime(args)


def escape_filter(value, args, env):
    """Takes a string and escapes it"""
    return cgi.escape(value)


DEFAULT_FILTERS = {
    'datetime_filter': datetime_filter,
    'escape_filter': escape_filter
}


class DenTemplate(object):
    # FIXME - This probably has problems with strings that have these
    # characters in them.
    TAG_RE = re.compile(r'(\{%[^%]+%\}' + r'|' + r'\{\{.+?\}\})')

    def parse_part(self, template, parts_left):
        """
        :returns: Block
        """
        children = []

        if parts_left[0].startswith('{%'):
            startblock = parts_left.pop(0)[2:-2].strip()
        else:
            startblock = None

        while parts_left:
            part = parts_left[0]

            if part.startswith('{{'):
                part = part[2:-2].strip()
                children.append(EvalExp(part))
                parts_left.pop(0)

            elif part.startswith('{%'):
                part = part[2:-2].strip()

                if part.startswith('if '):
                    children.append(
                        self.parse_part(template, parts_left)
                    )

                elif part == 'else':
                    if not startblock.startswith('if '):
                        raise ParseError('else found with no preceding if block')

                    # An "else" is really just a "if not(exp)", so
                    # we do that
                    parts_left[0] = (
                        '{% if not ' + startblock[2:].strip() + ' %}')
                    elseblock = self.parse_part(template, parts_left)
                    return Block('', [
                        IfBlock(startblock, children),
                        elseblock
                    ])

                elif part == 'endif':
                    if not startblock.startswith('if '):
                        raise ParseError('endif found with no preceding if block')

                    parts_left.pop(0)
                    return IfBlock(startblock, children)

                elif part.startswith('for '):
                    children.append(self.parse_part(template, parts_left))

                elif part == 'endfor':
                    if not startblock.startswith('for '):
                        raise ParseError('endfor found with no preceding for block')

                    parts_left.pop(0)
                    return ForBlock(startblock, children)

                else:
                    raise ParseError('unknown start block "{0}"'.format(part))

            else:
                children.append(Text(part))
                parts_left.pop(0)

        return Block(u'', children)

    def parse(self, template):
        parts = self.TAG_RE.split(template)
        return self.parse_part(template, list(parts))

    def templatize(self, template, env):
        new_env = {}
        new_env.update(DEFAULT_FILTERS)
        new_env.update(env)
        tree = self.parse(template)
        globalsdict = {}

        return tree.eval(globalsdict, new_env)
