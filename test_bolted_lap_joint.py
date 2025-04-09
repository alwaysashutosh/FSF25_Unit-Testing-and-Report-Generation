import pytest
from bolted_lap_joint_design import design_lap_joint
loads = list(range(0, 101, 10))
thicknesses = [6, 8, 10, 12, 16, 20, 24]

@pytest.mark.parametrize("P", loads)
@pytest.mark.parametrize("t1", thicknesses)
@pytest.mark.parametrize("t2", thicknesses)
def test_minimum_two_bolts(P, t1, t2):
    w = 150  

    try:
        result = design_lap_joint(P, w, t1, t2)
        num_bolts = result.get("number_of_bolts", 0)
        assert num_bolts >= 2, f"Failed for P={P} kN, t1={t1} mm, t2={t2} mm: only {num_bolts} bolt(s)"
    except ValueError:
        
        if P > 0:
            pytest.fail(f"No design found for P={P} kN, t1={t1} mm, t2={t2} mm")
