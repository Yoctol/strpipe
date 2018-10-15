from pathlib import Path


def get_pxd_path(pyx_path):
    pxd_path = Path(''.join(str(pyx_path).split('.')[:-1]) + '.pxd')
    if pxd_path.exists():
        return pxd_path
    return None
