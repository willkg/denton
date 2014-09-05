.. _templates:

=========
Templates
=========

Denton has a built-in templating engine that's kind of mediocre and
small. It allows for eval parts with ``{{`` and ``}}`` and also has
some rough blocks like ``if``, ``else``, and ``for``. It also has
support for eval filters.

Here's an example::

    Total entries: {{ len(content) }}

    {% if content %}
    {% for item in content %}
    **{{ item['created']|datetime('%c') }} :: {{ item['user']['name'] }}**
    http://standu.ps/status/{{ item['id'] }}

    {{ item['content'] }}


    {% endfor %}
    {% else %}
    Nothing happened.

    {% endif %}


Environment
===========

Locals dict is carried throughout so you can modify the environment as
you go along.


Whitespace (ugh!)
=================

Whitespace handling kind of sucks. Best to left-align all block tags
and give it an extra carriage return if you need one before and after
block tags.


Eval block
==========

You can evaluate things by wrapping the expression with ``{{`` and ``}}``.
The unicode representation of the result is returned.

This is commonly used for variables and accessing dicts/lists.

Examples::

    {{ name }}
    {{ item['created'] }}    


Eval block filters
==================

You can use a ``|`` in an eval block and apply filters to the result.

Available filters:

datetime
    Takes a strftime-style set of directives as a string and formats
    the date/datetime accordingly.

    Examples::

        {{ item['created']|datetime('%c') }}
        {{ item['created']|datetime('%Y-%m-%d') }}

escape
    Escapes text converting ``<`` to ``&lt;`` and ``>`` to ``&gt;``.

    Example::

        {{ item['title']|escape }}

    This is useful if you're writing HTML email templates.


If block
========

You can perform conditionals in the template using ``if``. Syntax is::

    {% if <expression> %}
    ...
    {% endif %}


The expression is evaluated in the environment and if truthy, will
parse the if block. If falsey, it will not parse the if block.

If blocks can also have else blocks::

    {% if <expression> %}
    ...
    {% else %}
    ...
    {% endif %}

This is shorthand for the following::

    {% if <expression> %}
    ...
    {% endif %}
    {% if not <expression> %}
    ...
    {% endif %}

Example::

    {% if content %}
    {% for item in content %}
    {{ item['title'] %}
    {% endfor %}
    {% else %}
    Nothing!
    {% endif %}


For block
=========

You can loop over iterables like lists using the ``for`` block. Syntax
is::

    {% for <var> in <expression> %}

The ``var`` will be the name in the environment you can use to access the
value for that iteration.

Example::

    {% for i in range(10) %}
    ...
    {% endfor %}

    {% for item in content %}
    ...
    {% endfor %}


Examples
========

Example template::

    Total entries: {{ len(content) }}

    {% if content %}
    {% for item in content %}
    **{{ item.get('project', {}).get('name', 'NONE')}} :: {{ item['created'] }} :: {{ item['user']['name'] }}**
    http://standu.ps/status/{{ item['id'] }}

    {{ item['content'] }}



    {% endfor %}
    {% else %}
    No one did shit.

    {% endif %}


HTML example::

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>{{ subject }}</title>
    <style type="text/css">
    /* Client-specific Styles */
    #outlook a {
    padding:0;
    } /* Force Outlook to provide a "view in browser" menu link. */

    body{
    color: #333;
    font-family: Helvetica, Arial, sans-serif;
    margin:0;
    padding:0;
    -webkit-text-size-adjust:100%;
    -ms-text-size-adjust:100%;
    width:100% !important;
    }
    
    /*
    Prevent Webkit and Windows Mobile platforms from changing default font
    sizes, while not breaking desktop design.
    */
    .ExternalClass {
    width:100%;
    } /* Force Hotmail to display emails at full width */
    
    .ExternalClass,
    .ExternalClass p,
    .ExternalClass span,
    .ExternalClass font,
    .ExternalClass td,
    .ExternalClass div {
    line-height: 100%;
    } /* Force Hotmail to display normal line spacing. */
    
    #background-table {
    background: #eaeff2;
    line-height: 100% !important;
    margin:0;
    padding:0;
    width:100% !important;
    }
    /* End reset */
    
    /*
    Yahoo paragraph fix: removes the proper spacing or the paragraph (p) tag.
    To correct we set the top/bottom margin to 1em in the head of the
    document. Simple fix with little effect on other styling. NOTE: It is
    also common to use two breaks instead of the paragraph tag but I think
    this way is cleaner and more semantic. NOTE: This example recommends 1em.
    More info on setting web defaults: http://www.w3.org/TR/CSS21/sample.html
    or http://meiert.com/en/blog/20070922/user-agent-style-sheets/
    */
    p {
    margin: 1em 0;
    /*
    Hotmail header color reset: Hotmail replaces your header color styles
    with a green color on H2, H3, H4, H5, and H6 tags. In this example, the
    color is reset to black for a non-linked header, blue for a linked
    header, red for an active header (limited support), and purple for a
    visited header (limited support). Replace with your choice of color.
    The !important is really what is overriding Hotmail's styling. Hotmail
    also sets the H1 and H2 tags to the same size.
    */
    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
    color: #333 !important;
    }
    
    h1 a,
    h2 a,
    h3 a,
    h4 a,
    h5 a,
    h6 a {
    color: #0095dd !important;
    }
    
    h1 a:active,
    h2 a:active,
    h3 a:active,
    h4 a:active,
    h5 a:active,
    h6 a:active {
    color: #0095dd !important;
    }
    
    h1 a:visited,
    h2 a:visited,
    h3 a:visited,
    h4 a:visited,
    h5 a:visited,
    h6 a:visited {
    color: #0095dd !important;
    }
    
    table td {
    border-collapse: collapse;
    }
    
    table {
    border-collapse:collapse;
    mso-table-lspace:0pt;
    mso-table-rspace:0pt;
    }
    a {
    color: #0095dd;
    text-decoration: none;
    }
    
    #main {
    margin: 0 1em 0 1em;
    }
    
    #main tbody td {
    background: #fff;
    padding: 30px;
    }
    
    #main thead th {
    font-size: 15px;
    padding: 16px 16px;
    text-align: left;
    }
    
    #main tfoot td {
    font-size: 13px;
    padding: 16px 30px 32px 30px;
    }
    
    .quote {
    border-left: 5px solid #eee;
    margin: 1em 0;
    padding: 10px 0 10px 20px;
    }
    
    .quote img {
    max-width: 100%;
    }
    
    .pre {
    font-family: monospace;
    white-space: pre;
    }
    
    .email-prefs {
    float: left;
    }
    
    .watch-link {
    float: right;
    }
    
    .email-prefs,
    .watch-link a {
    color: #999;
    font-size: 12px;
    }
    h1 {
    color: #525252;
    font-size: 24px;
    font-weight: normal;
    line-height: 28px;
    margin: 20px 0;
    }
    
    .user-meta {
    color: #525252;
    font-weight: normal;
    }
    
    .gi-box {
    border-bottom: 1px dashed #bbb;
    border-top: 1px dashed #bbb;
    line-height: 120%;
    margin-bottom: 30px;
    padding: 24px 10px;
    }
    
    div.tags .tag {
    color: #999;
    }
    
    div.tags .tag-block,
    div.tags .tag-blocked {
    color: red;
    }
    
    div.tags .tag-mfbt {
    color: blue;
    }
    
    #main thead th {
    padding-bottom: 0;
    padding-left: 0;
    padding-right: 0;
    }
    
    #main tfoot td {
    padding-left: 0;
    padding-right: 0;
    }
    </style>
    </head>
    <body>
    <table cellpadding="0" cellspacing="0" border="0" id="background-table">
    <tr>
    <td>
    <table cellpadding="0" cellspacing="0" border="0" align="center" id="main">
    <thead>
    <tr>
    <th>
    <h1>{{ subject }}</h1>
    </th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <td>
    {% if content %}
    {% for item in content %}
    <div class="user-meta">
    <strong>
    To {{ item.get('project', {}).get('name', 'NONE') }} at {{ item['created'] }} by {{ item['user']['name'] }}<br />
    </strong>
    <a href="http://standu.ps/status/{{ item['id'] }}">http://standu.ps/status/{{ item['id'] }}</a>
    </div>
    <div class="quote">
    {{ item['content'] }}
    </div>
    {% endfor %}
    {% else %}
    <p>No one did shit.</p>
    {% endif %}
    </td>
    </tr>
    </tbody>
    <tfoot>
    <tr>
    <td>
    <div class="gi-box">
    Built with Denton {{ dentonver }}: <a href="{{ dentonurl }}">{{ dentonurl }}</a>
    </div>
    </td>
    </tr>
    </tfoot>
    </table>
    </td>
    </tr>
    </table>
    </body>
    </html>
