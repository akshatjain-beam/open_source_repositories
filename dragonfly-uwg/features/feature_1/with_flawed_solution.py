```
        try:
            from honeybee_energy.room import Room2D
            from collections import Counter
            room_program_types = (
                room.energy.program_type for room in self.host.rooms
                if hasattr(room, 'energy') and hasattr(room.energy, 'program_type')
            )
            most_common_program = Counter(room_program_types).most_common(1)[0][0]
            for program in self.PROGRAMS:
                if program.lower() in most_common_program.lower():
                    self.program = program
                    break
        except ImportError:
            pass
```