import sys
import dspy
import toml
import os

# print(sys.prefix)
# print(sys.path[0])
# print(sys.base_prefix)

def Virtualenvcheck():
    venvpath=sys.prefix
    basepath=sys.path[0]
    base=sys.base_prefix

    # print(venvpath)
    # print(basepath)
    # print(base)

    if venvpath==base:
        return None
    elif venvpath == basepath:
        return None
    else:
        envname=venvpath.replace(basepath,"")
        return "Virtual Environment is :" + envname

print(Virtualenvcheck())

