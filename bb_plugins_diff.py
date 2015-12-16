"""
 Copyright (C) by GiastFader
 Releases under GPL2 License
 License: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html GPL version 2
"""

import sys, os, time, difflib, optparse
import collections
import requests

from requests.auth import HTTPBasicAuth
import json
import pprint
import StringIO
import codecs


def load_plugins_from_bb (result,bb_url,appcode,adminpwd,other_bb_url):
    baasbox_auth = HTTPBasicAuth("admin", adminpwd)
    r = requests.get(bb_url + "/admin/plugin" , headers={'X-BAASBOX-APPCODE':appcode}, auth=baasbox_auth)
    response = r.json()
    plugins = response["data"]
    for plugin in plugins:
        if not plugin["name"] in result:
            result[plugin["name"]] = {}
        result[plugin["name"]][bb_url] = plugin["code"][0]
        if not other_bb_url in result[plugin["name"]]:
            result[plugin["name"]][other_bb_url] = ""
    return result

def calculate_diff(plugins,options):
    od_plugins = collections.OrderedDict(sorted(plugins.items()))
    diff = ""
    for plugin_name, plugin_code in od_plugins.iteritems():
        ks = list(plugin_code)
        fromlines = StringIO.StringIO(plugin_code[ks[0]]).readlines()
        tolines = StringIO.StringIO(plugin_code[ks[1]]).readlines()
        now = time.time()
        fromdate = now
        todate = now
        fromfile = ks[0] + ": " + plugin_name
        tofile = ks[1] + ": " + plugin_name
        
        if options.u:
            diff += ''.join(difflib.unified_diff(fromlines, tolines, fromfile, tofile,
                                    fromdate, todate, n=options.lines))
        elif options.n:
            diff += ''.join(difflib.ndiff(fromlines, tolines))
        elif options.m:
            diff += difflib.HtmlDiff().make_table(
                                    fromlines,
                                    tolines,
                                    " " + fromfile + " ",
                                    " " + tofile + " ",
                                    context=options.c,
                                    numlines=options.lines) + "<br /> <p />"
        else:
            diff += ''.join(difflib.context_diff(fromlines, tolines, fromfile, tofile,
                                        fromdate, todate, n=options.lines))
        
    return diff

def concatenate_header_and_footer(html_tables):
    to_ret = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

            <html>

                <head>
                        <meta http-equiv="Content-Type"
                            content="text/html; charset=ISO-8859-1" />
                        <title></title>
                        <style type="text/css">
                            table.diff {font-family:Courier; border:medium;}
                            .diff_header {background-color:#e0e0e0}
                            td.diff_header {text-align:right}
                            .diff_next {background-color:#c0c0c0}
                            .diff_add {background-color:#aaffaa}
                            .diff_chg {background-color:#ffff77}
                            .diff_sub {background-color:#ffaaaa}
                        </style>
                </head> 
                <table class="diff" summary="Legends">
                <tr> <th colspan="2"> Legends </th> </tr>
                <tr> <td> <table border="" summary="Colors">
                <tr><th> Colors </th> </tr>
                <tr><td class="diff_add">&nbsp;Added&nbsp;</td></tr>
                <tr><td class="diff_chg">Changed</td> </tr>
                <tr><td class="diff_sub">Deleted</td> </tr>
                </table></td>
                <td> <table border="" summary="Links">
                <tr><th colspan="2"> Links </th> </tr>
                <tr><td>(f)irst change</td> </tr>
                <tr><td>(n)ext change</td> </tr>
                <tr><td>(t)op</td> </tr>
                </table></td> </tr>
        </table> <p />""" + html_tables
    
    to_ret += """<table class="diff" summary="Legends">
        <tr> <th colspan="2"> Legends </th> </tr>
        <tr> <td> <table border="" summary="Colors">
        <tr><th> Colors </th> </tr>
        <tr><td class="diff_add">&nbsp;Added&nbsp;</td></tr>
        <tr><td class="diff_chg">Changed</td> </tr>
        <tr><td class="diff_sub">Deleted</td> </tr>
        </table></td>
        <td> <table border="" summary="Links">
        <tr><th colspan="2"> Links </th> </tr>
        <tr><td>(f)irst change</td> </tr>
        <tr><td>(n)ext change</td> </tr>
        <tr><td>(t)op</td> </tr>
        </table></td> </tr>
        </table>
        </body>
        
        </html>"""
    return to_ret

def main():
    # Configure the option parser
    usage = "usage: %prog [options] bb_url1 appcode1 adminpwd1 bb_url2 appcode2 adminpwd2"
    parser = optparse.OptionParser(usage)
    parser.add_option("-c", action="store_true", default=False,
                          help='Produce a context format diff (default)')
    parser.add_option("-u", action="store_true", default=False,
                      help='Produce a unified format diff')
    hlp = 'Produce HTML side by side diff (can use -c and -l in conjunction)'
    parser.add_option("-m", action="store_true", default=False, help=hlp)
    parser.add_option("-n", action="store_true", default=False,
                      help='Produce a ndiff format diff')
    parser.add_option("-l", "--lines", type="int", default=3,
                      help='Set number of context lines (default 3)')
                      
                      
    (options, args) = parser.parse_args()

    if len(args) == 0:
        parser.print_help()
        sys.exit(1)

    if len(args) != 6:
        parser.error("need to specify both BaasBox(es) credentials")

    n = options.lines
    bb_url1, appcode1, adminpwd1, bb_url2, appcode2, adminpwd2 = args # as specified in the usage string

    result = {}
    plugins1 = load_plugins_from_bb(result,bb_url1,appcode1,adminpwd1,bb_url2)
    plugins2 = load_plugins_from_bb(result,bb_url2,appcode2,adminpwd2,bb_url1)

    diff = calculate_diff (result,options)
    if options.m:
        diff = concatenate_header_and_footer (diff)

    UTF8Writer = codecs.getwriter('utf8')
    sys.stdout = UTF8Writer(sys.stdout)
    sys.stdout.writelines(diff)

if __name__ == '__main__':
    main()
