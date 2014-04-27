import StringIO
import json
import re
import sys
import urllib2


def request_url(url, is_json=False):
    resp = urllib2.urlopen(url)

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
    def __init__(self, exp):
        self.exp = exp

    def eval(self, globalsdict, env):
        # FIXME: support filters here
        return unicode(eval(self.exp, globalsdict, env))


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


class DenTemplate(object):
    # FIXME - This probably has problems with strings that have these
    # characters in them.
    TAG_RE = re.compile(r'(\{%[^%]+%\}' + r'|' + r'\{\{[^\}]+\}\})')

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
        tree = self.parse(template)
        globalsdict = {}

        return tree.eval(globalsdict, env)
