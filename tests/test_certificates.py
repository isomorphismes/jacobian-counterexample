import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "artifacts" / "sympy" / "verify.py"
SPEC = importlib.util.spec_from_file_location("jacobian_verify", SCRIPT)
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VERIFY)

PLANE_SCRIPT = (
    Path(__file__).parents[1] / "artifacts" / "sympy" / "verify_plane_attack.py"
)
PLANE_SPEC = importlib.util.spec_from_file_location("plane_attack_verify", PLANE_SCRIPT)
PLANE_VERIFY = importlib.util.module_from_spec(PLANE_SPEC)
assert PLANE_SPEC.loader is not None
PLANE_SPEC.loader.exec_module(PLANE_VERIFY)


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


def test_equivariant_plane_quotient():
    PLANE_VERIFY.certify_equivariant_quotient()


def test_linear_slice_formula():
    PLANE_VERIFY.certify_linear_slice_formula()


def test_marked_plane_differential_identity():
    PLANE_VERIFY.certify_marked_plane_differential_identity()


def test_nonlinear_collision_graph_obstruction():
    PLANE_VERIFY.certify_nonlinear_collision_graph_obstruction()


def test_equivariant_nonlinear_slice_obstructions():
    PLANE_VERIFY.certify_equivariant_nonlinear_slice_obstructions()


def test_octahedral_sextic_model():
    PLANE_VERIFY.certify_octahedral_sextic_model()
