"""
Usage: cli2web.py [options] [script]
cli2web creates a web interface for a given Python script that uses argparse
for the CLI.

Examples:
cli2web.py my_script.py #creates web interface for my_script.py

Options:
I haven't decided on these yet
"""

import os
import pprint
import argparse
import imp
from bottle import template, get, post, run, request
from subprocess import call

#ArgumentParser description. The object is kept global so that it remains
#accessible for import and therefore cli2web can work from a self-generated
#web interaface.
desc = ("Creates a web interface for a given Python script that uses "
        "argparse for CLI.")
parser = argparse.ArgumentParser(description=desc)
parser.add_argument('script', type=file)

context = {}

def run_script(script, argparse, args):
    """Run the given script after properly formatting the input
    with the given argparse objects and args"""
    # format the arguments - positional and optional!
    args = args
    call(['python'] + [script] + args)

@get('/')
def index():
    return template('form', **context)

@post('/')
def form():
    # Now we can access the post data, we just need to plug it into the cli
    # script, run the thing and return results!
    result = "coming soon!"
    return result

def main():
    args = parser.parse_args()
    root, ext = os.path.splitext(args.script.name)
    if not ext == '.py':
        parser.error('Not a Python script!')
    module = imp.load_source('', args.script.name)
    for sym in dir(module):
        obj = getattr(module, sym)
        if isinstance(obj, argparse.ArgumentParser):
            #pp = pprint.PrettyPrinter(indent=4)
            #pp.pprint(obj.__dict__)
            #print template(html, **obj.__dict__)
            global context
            context = obj.__dict__
            print template('form', **context)
    run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    main()
