import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "artifacts" / "sympy" / "verify.py"
SPEC = importlib.util.spec_from_file_location("jacobian_verify", SCRIPT)
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VERIFY)


def test_direct_certificate():
    VERIFY.certify_direct()


def test_structural_certificate():
    VERIFY.certify_structural_determinant()


def test_fiber_certificate():
    VERIFY.certify_fiber_ideal()


def test_normalized_certificate():
    VERIFY.certify_normalization()


def test_x_elimination_certificate():
    VERIFY.certify_x_elimination()


def test_binary_cubic_geometry():
    VERIFY.certify_binary_cubic_geometry()


def test_nonproperness_certificate():
    VERIFY.certify_escape_curve()


def test_weyl_endomorphism_relations():
    VERIFY.certify_weyl_relations()
