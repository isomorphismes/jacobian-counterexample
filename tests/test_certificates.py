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

RESULTANT_SCRIPT = (
    Path(__file__).parents[1] / "artifacts" / "sympy" / "verify_resultant_route.py"
)
RESULTANT_SPEC = importlib.util.spec_from_file_location(
    "resultant_route_verify", RESULTANT_SCRIPT
)
RESULTANT_VERIFY = importlib.util.module_from_spec(RESULTANT_SPEC)
assert RESULTANT_SPEC.loader is not None
RESULTANT_SPEC.loader.exec_module(RESULTANT_VERIFY)

PSEUDOPLANE_SCRIPT = (
    Path(__file__).parents[1] / "research" / "n2" / "certify_pseudoplane_poisson.py"
)
PSEUDOPLANE_SPEC = importlib.util.spec_from_file_location(
    "pseudoplane_poisson_verify", PSEUDOPLANE_SCRIPT
)
PSEUDOPLANE_VERIFY = importlib.util.module_from_spec(PSEUDOPLANE_SPEC)
assert PSEUDOPLANE_SPEC.loader is not None
PSEUDOPLANE_SPEC.loader.exec_module(PSEUDOPLANE_VERIFY)


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


def test_lou_left_right_equivalence_and_factor_chart():
    RESULTANT_VERIFY.certify_lou_left_right_equivalence_and_chart()


def test_general_resultant_jacobians():
    RESULTANT_VERIFY.certify_resultant_jacobians()


def test_literal_quadratic_factor_collapse():
    RESULTANT_VERIFY.certify_literal_quadratic_collapse()


def test_weighted_plane_core():
    RESULTANT_VERIFY.certify_weighted_plane_core()


def test_quintic_slice_obstructions():
    RESULTANT_VERIFY.certify_quintic_slice_obstructions()


def test_quartic_factor_scaffold():
    RESULTANT_VERIFY.certify_quartic_factor_scaffold()


def test_pseudoplane_darboux_charts():
    PSEUDOPLANE_VERIFY.certify_poisson_and_darboux_charts()


def test_pseudoplane_homogeneous_no_go_formulas():
    PSEUDOPLANE_VERIFY.certify_homogeneous_formulas()


def test_pseudoplane_ambient_quadratic_no_go():
    PSEUDOPLANE_VERIFY.certify_no_ambient_quadratic_pair()


def test_pseudoplane_lnd_and_self_map():
    PSEUDOPLANE_VERIFY.certify_lnd_and_self_map_identities()
