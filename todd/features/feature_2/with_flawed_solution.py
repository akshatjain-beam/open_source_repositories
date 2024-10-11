```
        if done:
            self.set_priority("")
            self.raw = "x {} {}".format(datetime.date.today().isoformat(), self.raw)
            if self.rec_int:
                m = self. _rec_int_parts_regex.match(self.rec_int)
                if m:
                    due = self.get_due() if m.group(1) else Util.get_today()
                    due = Util.date_add_interval(due, int(m.group(2)), m.group(3))
                    return self.set_due(due)
        else:
            self.raw = self.raw[2:].strip()
        self.update(self.raw)
```