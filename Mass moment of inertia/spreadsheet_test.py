import unittest
import math
import numpy as np
import spreadsheet as ss


# Import the script you want to test here, so you can use its variables/functions below

class MyTestCase(unittest.TestCase):

    # Add tests you want to run here. Make sure you clearly define and justify (Somewhere) the variables used
    # Delete sample tests shown below:
    # All test function names should start with 'test', otherwise they will not run!
    def test_center_of_gravity(self):
        m = np.array([[0.5], [0.4], [0.3], [0.2], [0.1]])
        x = np.array([[0.5], [-0.4], [0.3], [0.2], [0.1]])
        y = np.array([[0.5], [0.4], [0.3], [-0.2], [0.1]])
        z = np.array([[0.5], [0.4], [0.3], [0.2], [-0.1]])

        programmed_result = ss.center_of_gravity(m, x, y, z)
        calculated_result = 0.15333333, 0.31333333, 0.35333333
        digits = 8

        self.assertEqual(len(programmed_result), len(calculated_result))
        for i in range(len(calculated_result)):
            self.assertAlmostEqual(programmed_result[i], calculated_result[i], places=digits)

    def test_vehicle_to_body_reference_frame(self):
        x, y, z = 0.1, -20., -5.6
        cg = (0.5, -.6, -9)

        programmed_result = ss.vehicle_to_body_reference_frame(x, y, z, cg)
        calculated_result = 20.5, -0.7, -14.6
        digits = 8

        self.assertEqual(len(programmed_result), len(calculated_result))
        for i in range(len(calculated_result)):
            self.assertAlmostEqual(programmed_result[i], calculated_result[i], places=digits)

    def test_mass_moment_of_inertia_cuboid(self):
        mass, width, depth, height = 14., .00056, 0.78, 11245.34
        programmed_result = ss.mass_moment_of_inertia_cuboid(mass, width, depth, height)
        calculated_result = np.array([[147533951.0446666, 0.0, 0.0], [0.0, 0.7098003658666, 0.0],
                                      [0.0, 0.0, 147533950.33486703253333]])
        self.assertEqual(np.allclose(programmed_result, calculated_result), True)

    def test_mass_moment_of_inertia_steiner(self):
        mass, x, y, z = 14., .00056, 0.78, 11245.34
        programmed_result = ss.mass_moment_of_inertia_steiner(mass, x, y, z)
        calculated_result = np.array([[0.0000043904, 0.0061152, 88.1634656], [0.0061152, 8.5176, 122799.1128],
                                      [88.1634656, 122799.1128, 1770407404.0184]])
        self.assertEqual(np.allclose(programmed_result, calculated_result), True)

    def test_width_of_landing_gear_from_tip_over_angle(self):
        tip_over_angle, cg_z = 30, 0.20
        programmed_result = ss.width_of_landing_gear_from_tip_over_angle(tip_over_angle, cg_z)
        calculated_result = 0.2309
        digits = 4
        self.assertAlmostEqual(programmed_result, calculated_result, places=digits)

    def test_tip_over_angle_from_width_of_landing_gear(self):
        width_of_landing_gear, cg_z = 0.30, 0.20
        programmed_result = ss.tip_over_angle_from_width_of_landing_gear(width_of_landing_gear, cg_z)
        calculated_result = 36.87
        digits = 2
        self.assertAlmostEqual(programmed_result, calculated_result, places=digits)


if __name__ == '__main__':
    unittest.main()
