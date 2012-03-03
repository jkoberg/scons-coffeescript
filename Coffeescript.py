
import re

def exists(env):
    return env.Execute('coffee --version')

def generate(env):
    coffee_scan = env.Scanner(
        function = coffee_scan_func,
        skeys = ['.coffee', '.js']
        )

    coffee_builder = env.Builder(
        action='coffee -cs  < $$SOURCE > $$TARGET',
        suffix='.js',
        src_suffix='.coffee',
        single_source = True,
        source_scanner = coffee_scan
        )
    env.Append(COFFEEROOT=env.Dir('.'))
    env.Append(BUILDERS={'Coffeescript': coffee_builder})
    env.Append(SCANNERS=coffee_scan)
    
    
r"""data-main\w*=\w*(['"])(.+?)\1"""

require_patterns = [
    re.compile(pattern, re.MULTILINE )
    for pattern in [
        r"""require\s*\(*\s*['"]([^.].*?)['"]\)*""",
        r"""require\s*\(*\s*['"](\./.*?)['"]\)*""",
        r"""require\s*\(*\s*['"](\.\./.*?)['"]\)*""",
        ]
    ]
    
define_patterns = [
    re.compile(pattern, re.MULTILINE )
    for pattern in [
        r"""define\s*\(*\s*\[(.+?)\]""",
        r"""require\s*\(*\s*\[(.+?)\]""",
        ]
    ]
    
    
def glob_requirement_name(env, node, name):
    if not name.startswith('_'):
        if name.endswith('.js'):
            # suffixed files are located relative to the script calling require()
            # that seems wrong. Suffixed files are located relative to root???
            #req = node.File(name)
            yield env['COFFEEROOT'].File(name)
        else:
            # non-suffixed files are located relative to html containing data-main
            # Also seems wrong. They are located relative to the SCRIPT mentioned in data-main
            coffee_file = node.File(name+'.coffee')
            if coffee_file.exists():
                # build the required JS file from the coffescript source
                reqs = env.Coffeescript(source=coffee_file)
                for req in reqs:
                    yield req
            else:
                # if no .coffee to compile, depend on a raw .js
                yield node.File(name+'.js')
    


    
def coffee_scan_func(node, env, path):
    
    contents = node.get_text_contents()
    requirements = []
    
    for pattern in require_patterns:
        for match in pattern.finditer(contents):
            requirement = match.group(1)
            for found in glob_requirement_name(env, node, requirement):
                yield found
                
    for pattern in define_patterns:
        for match in pattern.finditer(contents):
            define_strings = [s.strip().strip('"\'') for s in match.group(1).split(',')]
            for requirement in define_strings:
                for found in glob_requirement_name(env, node, requirement):
                    yield found
        





