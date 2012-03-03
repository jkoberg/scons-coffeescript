

These are SCons build tools for Coffeescript files.

In normal use, the Coffeescript.py file would go into ./site_scons/site_tools/,
and an SConstruct file would be placed in the project root that sets up a
build.


SConstruct::

    import os
    
    env = DefaultEnvironment(
            tools = ['Coffeescript'],
            ENV = dict(
                PATH = os.environ['PATH'],
                )
            )
    
    env.SConscript(dirs=['js'], exports=['env'])
    

    
js/SConscript::

    Import('env')
    
    coffee_files = env.Glob('*.coffee')
    
    js_files = env.Coffeescript(coffee_files)
    
