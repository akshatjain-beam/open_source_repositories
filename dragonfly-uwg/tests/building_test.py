import unittest
from unittest.mock import MagicMock
from dragonfly_uwg.properties.building import BuildingUWGProperties

class TestBuildingUWGProperties(unittest.TestCase):

    def setUp(self):
        """Set up the test environment for each test."""
        self.host = MagicMock()
        self.building_properties = BuildingUWGProperties(self.host)

    def test_infer_program_from_energy_program_mixed_types(self):
        """
        Test program inference when multiple room types exist,
        with one being the most common. The expected outcome is
        that the building's program is set to the most frequent
        room type, which is 'MediumOffice' in this case.
        """
        room1 = MagicMock()
        room1.properties.energy.program_type.identifier = 'MediumOffice'
        room2 = MagicMock()
        room2.properties.energy.program_type.identifier = 'MediumOffice'
        room3 = MagicMock()
        room3.properties.energy.program_type.identifier = 'SmallOffice'
        
        # Assign mock rooms to the host
        self.host.unique_room_2ds = [room1, room2, room3]
        
        # Invoke the method
        self.building_properties.infer_program_from_energy_program()
        
        # Check if the program was updated to the most common type
        self.assertEqual(self.building_properties.program, 'MediumOffice')



    def test_infer_program_from_energy_program_all_same_type(self):
        """
        Test inference when all rooms are of the same program type.
        This case checks if the building's program is set correctly
        when every room type matches; here, it should be 'SmallHotel'.
        """
        room1 = MagicMock()
        room1.properties.energy.program_type.identifier = 'SmallHotel'
        room2 = MagicMock()
        room2.properties.energy.program_type.identifier = 'SmallHotel'
        room3 = MagicMock()
        room3.properties.energy.program_type.identifier = 'SmallHotel'
        
        # Assign mock rooms to the host
        self.host.unique_room_2ds = [room1, room2, room3]
        
        # Invoke the method
        self.building_properties.infer_program_from_energy_program()
        
        # Check if the program was updated to the common type
        self.assertEqual(self.building_properties.program, 'SmallHotel')

    def test_infer_program_from_energy_program_programs_with_substrings(self):
        """
        Test behavior when room identifiers contain substrings of
        valid UWG programs. This test ensures that the inference
        method can identify the longest matching program type
        when substrings are present, expecting 'LargeOffice' 
        as the inferred program type.
        """
        room1 = MagicMock()
        room1.properties.energy.program_type.identifier = 'LargeOfficeWithMeetingRooms'
        room2 = MagicMock()
        room2.properties.energy.program_type.identifier = 'LargeOfficeAndLounge'
        room3 = MagicMock()
        room3.properties.energy.program_type.identifier = 'OfficeSpace'
        
        # Assign mock rooms to the host
        self.host.unique_room_2ds = [room1, room2, room3]
        
        # Invoke the method
        self.building_properties.infer_program_from_energy_program()
        
        # Check that the program is inferred correctly
        self.assertEqual(self.building_properties.program, 'LargeOffice')

    def test_infer_program_from_energy_program_multiple_room_types(self):
        """
        Test inference with multiple room types where one type
        is predominant. This test checks that the building's program
        is set to the most frequent room type, which should be
        'LargeOffice' since there are two rooms of that type.
        """
        room1 = MagicMock()
        room1.properties.energy.program_type.identifier = 'LargeOffice'
        room2 = MagicMock()
        room2.properties.energy.program_type.identifier = 'LargeOffice'
        room3 = MagicMock()
        room3.properties.energy.program_type.identifier = 'MediumOffice'
        
        # Assign mock rooms to the host
        self.host.unique_room_2ds = [room1, room2, room3]
        
        # Invoke the method
        self.building_properties.infer_program_from_energy_program()
        
        # Program should be set to the most common type
        self.assertEqual(self.building_properties.program, 'LargeOffice')

    def test_infer_program_from_energy_program_no_matching_program(self):
        """
        Test behavior when room types don't match any UWG programs.
        This test checks if the program remains unchanged when
        no recognized room types are present, expecting it to
        remain as the default value of 'LargeOffice'.
        """
        room1 = MagicMock()
        room1.properties.energy.program_type.identifier = 'Gym'
        room2 = MagicMock()
        room2.properties.energy.program_type.identifier = 'Library'
        
        # Assign mock rooms to the host
        self.host.unique_room_2ds = [room1, room2]
        
        # Invoke the method
        self.building_properties.infer_program_from_energy_program()
        
        # Program should remain unchanged
        self.assertEqual(self.building_properties.program, 'LargeOffice')

# Running the tests
if __name__ == '__main__':
    unittest.main()
