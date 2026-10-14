"""Extract reusable conditional setup without executing the historical runner."""
from textwrap import dedent
from apply_di7_ap_as_01 import R


def main():
    path=R/'tools/di7_area_fixtures.py'; assert not path.exists()
    source=(R/'tools/validate_di7_area_geometry.py').read_text(encoding='utf-8')
    start=source.index('    def volume('); end=source.index('    def paid(',start)
    text=dedent(source[start:end])
    assert text.count("def make(sid='mass-revelation'")==1
    text=text.replace("def make(sid='mass-revelation'","def make(sources,sid='mass-revelation'",1)
    text='"""Explicit conditional caster/geometry fixtures, not authored character records."""\nfrom copy import deepcopy\nfrom di7_area_geometry import AreaGeometryTransactions\n\n'+text
    compile(text,str(path),'exec'); path.write_text(text,encoding='utf-8',newline='\n')
    print('Created reusable conditional fixtures; historical validator unchanged.')


if __name__=='__main__': main()
