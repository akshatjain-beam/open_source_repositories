```
        if done:
            self.set_priority("")
            self.raw = "x {0} {1}".format(Util.get_today_str(), self.raw)
            if self.rec_int:
                (prefix, value, itype) = Util._rec_int_parts_regex.match(self.rec_int).groups()
                value = int(value)
                if prefix != "+":
                    new_due = Util.get_today()
                else:
                    new_due = self.get_due()
                new_due = Util.date_add_interval(new_due, itype, value)
                self.set_due(new_due)
                return new_due
        else:
            self.raw = re.sub(Task._done_regex, "", self.raw)
        self.update(self.raw)
        return None
```