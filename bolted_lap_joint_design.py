import math
import IS800_2007
from IS800_2007 import IS800_2007
import math

is800 = IS800_2007()

bolt_fu = 400  # MPa – ultimate tensile strength of bolt
bolt_dia = 16  # mm – example
A_bolt = math.pi * (bolt_dia ** 2) / 4

V_b = is800.cl_10_3_3_bolt_shear_capacity(bolt_fu, A_bolt, A_bolt, 0, 0, 'field')
print("Bolt Shear Capacity (V_b):", V_b)



def design_lap_joint(P, w, t1, t2):
    """
    Design a bolted lap joint connecting two plates.
    :param P: Tensile force in kN
    :param w: Width of the plates in mm
    :param t1: Thickness of plate 1 in mm
    :param t2: Thickness of plate 2 in mm
    :return: Dictionary of design parameters and results
    """

    # Convert tensile force to Newtons
    P_N = P * 1000

    # Available data
    d_list = [10, 12, 16, 20, 24]  # Bolt diameters in mm
    GB_list = [3.6, 4.6, 4.8, 5.6, 5.8]  # Bolt grades
    GP_list = ["E250", "E275", "E300", "E350", "E410"]  # Plate grades

    # Define a mapping from plate grade to yield and ultimate strength
    plate_grades = {
        "E250": (250, 410),
        "E275": (275, 440),
        "E300": (300, 470),
        "E350": (350, 510),
        "E410": (410, 550)
    }

    # Select the best plate grade based on the given thicknesses
    plate_grade = GP_list[-1]  # Choose the highest grade for the design
    fy_plate, fu_plate = plate_grades[plate_grade]  # Get the yield and ultimate strengths for the chosen grade

    # Initialize variables to store the best design
    best_design = None
    min_length = float('inf')

    for d in d_list:
        for GB in GB_list:
            # Calculate the bolt strength
            bolt_fu, bolt_fy = calculate_bolt_strength(GB)
            
            # Calculate the shear strength of one bolt
            A_bolt = math.pi * (d / 2) ** 2  # Cross-sectional area of the bolt
            V_b = is800.cl_10_3_3_bolt_shear_capacity(bolt_fu, A_bolt, A_bolt, 1, 0, 'field')

            
            # Calculate the required number of bolts
            N_b = math.ceil(P_N / (V_b * 0.75))  # Using a safety factor of 1.33
            
            if N_b < 2:
                continue  # Skip if the number of bolts is less than 3

            # Calculate distances
            e = d + 5  # End distance (typically 5 mm larger than bolt diameter)
            p = d + 10  # Pitch distance (typically 10 mm larger than bolt diameter)
            g = w / 2  # Gauge distance (for simplicity, use half of the plate width)

            # Calculate the length of the connection
            length_of_connection = w + 2 * e

            # Calculate the bearing strength of the bolt
            V_dpb = IS800_2007.cl_10_3_4_bolt_bearing_capacity(fu_plate, bolt_fu, t1 + t2, d, e, p, 'Standard', 'field')

            # Calculate the efficiency of the connection
            Utilization_ratio = P_N / (N_b * V_b * 0.75)  # Using a safety factor of 1.33
            
            # Check if this design is better
            if Utilization_ratio <= 1 and length_of_connection < min_length:
                min_length = length_of_connection
                best_design = {
                    "bolt_diameter": d,
                    "bolt_grade": GB,
                    "number_of_bolts": N_b,
                    "pitch_distance": p,
                    "gauge_distance": g,
                    "end_distance": e,
                    "edge_distance": e,
                    "number_of_rows": 1,  # Simple design assumption, can be improved
                    "number_of_columns": N_b,  # One column for simplicity
                    "hole_diameter": d + 2,  # Diameter of hole is slightly larger than the bolt
                    "strength_of_connection": N_b * V_b * 0.75,  # Strength based on shear capacity
                    "yield_strength_plate_1": fy_plate,
                    "yield_strength_plate_2": fy_plate,
                    "length_of_connection": length_of_connection,
                    "efficiency_of_connection": Utilization_ratio
                }

    if best_design is None:
        raise ValueError("No suitable design found that meets the requirements.")

    return best_design


def calculate_bolt_strength(bolt_grade):
    """
    Calculate the ultimate tensile strength and yield strength of the bolt based on its grade.
    :param bolt_grade: Bolt grade (e.g., 4.6, 5.6)
    :return: List containing [ultimate tensile strength, yield strength] of the bolt
    """
    bolt_fu = float(int(bolt_grade) * 100)  # Ultimate tensile strength (MPa)
    bolt_fy = float((bolt_grade - int(bolt_grade)) * bolt_fu)  # Yield strength (MPa)
    return [bolt_fu, bolt_fy]


# Example usage
if __name__ == "__main__":
    P = 100  # Tensile force in kN
    w = 150  # Width of the plates in mm
    t1 = 10  # Thickness of plate 1 in mm
    t2 = 12  # Thickness of plate 2 in mm

    design = design_lap_joint(P, w, t1, t2)
    for key, value in design.items():
        print(f"{key}: {value}")