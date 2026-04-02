"""Inject ibm_db_dll.pth into a wheel so it lands in site-packages on install.

Usage: python scripts/inject_pth_into_wheel.py <wheel_dir>

Wheels are zip files. Files at the root level of a wheel (alongside .py
modules) are installed to site-packages. This script adds ibm_db_dll.pth
to every .whl file in the given directory.
"""
import os, sys, hashlib, base64, zipfile, glob, tempfile, shutil

PTH_FILENAME = 'ibm_db_dll.pth'
PTH_CONTENT = 'import _ibm_db_register_dll\n'
REGISTER_MODULE = '_ibm_db_register_dll.py'


def _record_line(name, content_bytes):
    """Build a RECORD entry: name,sha256=<digest>,<length>"""
    digest = hashlib.sha256(content_bytes).digest()
    b64 = base64.urlsafe_b64encode(digest).rstrip(b'=').decode('ascii')
    return f'{name},sha256={b64},{len(content_bytes)}'


def inject_pth(whl_path):
    """Add ibm_db_dll.pth and _ibm_db_register_dll.py to a wheel file."""
    # Skip if already injected
    with zipfile.ZipFile(whl_path, 'r') as zin:
        if PTH_FILENAME in zin.namelist():
            print(f'  {PTH_FILENAME} already in {os.path.basename(whl_path)}, skipping')
            return

    # Read the register module from the repo root
    register_module_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), REGISTER_MODULE)
    with open(register_module_path, 'rb') as f:
        register_bytes = f.read()

    tmp_fd, tmp_path = tempfile.mkstemp(suffix='.whl')
    os.close(tmp_fd)

    pth_bytes = PTH_CONTENT.encode('utf-8')
    pth_record = _record_line(PTH_FILENAME, pth_bytes)
    register_record = _record_line(REGISTER_MODULE, register_bytes)

    with zipfile.ZipFile(whl_path, 'r') as zin, \
         zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as zout:

        for item in zin.infolist():
            data = zin.read(item.filename)

            # Append our entries to the RECORD file
            if item.filename.endswith('/RECORD'):
                data = data.rstrip(b'\n') + b'\n' + pth_record.encode('utf-8') + b'\n' + register_record.encode('utf-8') + b'\n'

            zout.writestr(item, data)

        # Add the .pth file and register module at the wheel root
        zout.writestr(PTH_FILENAME, pth_bytes)
        zout.writestr(REGISTER_MODULE, register_bytes)

    shutil.move(tmp_path, whl_path)
    print(f'  Injected {PTH_FILENAME} and {REGISTER_MODULE} into {os.path.basename(whl_path)}')


def main():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <wheel_dir>')
        sys.exit(1)

    wheel_dir = sys.argv[1]
    wheels = glob.glob(os.path.join(wheel_dir, '*.whl'))

    if not wheels:
        print(f'No .whl files found in {wheel_dir}')
        sys.exit(1)

    for whl in wheels:
        inject_pth(whl)

    print(f'Done: processed {len(wheels)} wheel(s)')


if __name__ == '__main__':
    main()
