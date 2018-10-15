import os.path as osp
from pathlib import Path

from ..get_pxd_path import get_pxd_path


HERE = osp.dirname(osp.abspath(__file__))


def test_get_pxd_path():
    path = Path(osp.join(HERE, 'file_w_pxd.pyx'))
    pxd_path = get_pxd_path(path)
    assert pxd_path is not None
    assert str(pxd_path) == osp.join(HERE, 'file_w_pxd.pxd')


def test_get_pxd_path_not_existed():

    path = Path(osp.join(HERE, 'file_wo_pxd.pyx'))
    pxd_path = get_pxd_path(path)
    assert pxd_path is None
