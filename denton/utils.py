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


class DenTemplate(object):
    def templatize(self, template, env):

        # FIXME - This probably has problems with strings that have these
        # characters in them.
        tags_re = re.compile(r'(\{%[^%]+%\}' + r'|' + r'\{\{[^\}]+\}\})')

        globalsdict = {}

        old_stdout = sys.stdout
        old_stderr = sys.stderr

        parts = tags_re.split(template)
        output = []

        try:
            for part in parts:
                if part.startswith('{{'):
                    # Nix the {{ and }} and strip whitespace
                    part = part[2:-2].strip()
                    output.append(str(eval(part, globalsdict, env)))

                elif part.startswith('{%'):
                    # FIXME - Create a better block structure here.

                    # Nix the {% and %}.
                    codeblock = part[2:-2].strip()

                    sys.stdout = StringIO.StringIO()
                    sys.stderr = StringIO.StringIO()

                    try:
                        exec codeblock  in env, globalsdict
                    except Exception as exc:
                        print 'ERROR in processing: {0}'.format(exc)

                    output.append(sys.stdout.getvalue() + sys.stderr.getvalue())

                else:
                    output.append(part)

        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        return ''.join(output).rstrip()
