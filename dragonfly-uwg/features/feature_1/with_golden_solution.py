```
        try:
            room_progs = [rm.properties.energy.program_type.identifier
                          for rm in self.host.unique_room_2ds]
        except AttributeError:  # dragonfly-energy extension is not installed
            room_progs = None
        if room_progs is not None:
            primary_prog = max(set(room_progs), key=room_progs.count)
            for prog in self.PROGRAMS:
                if prog in primary_prog:
                    self._program = prog
                    break
```