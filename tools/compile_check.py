import py_compile
import glob

files = [
    'app/main.py',
]
files += glob.glob('app/views/*.py')
files += glob.glob('app/services/*.py')

errs = []
for f in files:
    try:
        py_compile.compile(f, doraise=True)
        print('OK:', f)
    except Exception as e:
        print('ERR:', f, e)
        errs.append((f, str(e)))

if not errs:
    print('\nALL FILES COMPILED OK')
else:
    print('\nSOME FILES FAILED')
