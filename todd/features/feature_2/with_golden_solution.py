```
        if self.is_done() == done:
            return
        if done:
            self.set_priority("")
            today = datetime.date.today()
            self.update("x " + today.isoformat() + " " + self.raw)
            if self.rec_int:
                (prefix, value, itype) = Task._rec_int_parts_regex.match(self.rec_int).groups()
                value = int(value)
                date = self.get_due() if prefix == "+" else today
                return Util.date_add_interval(date, itype, value)
        else:
            self.update(re.sub(Task._done_regex, "", self.raw))
```