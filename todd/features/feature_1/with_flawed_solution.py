```
    def set_priority(self, new_priority):
        if self.priority == new_priority:
            return
        new_priority = "(" + new_priority + ") " if new_priority else ""
        if self.priority:
            self.raw = re.sub(Task._priority_regex, new_priority, self.raw)
        elif self.raw[0:2] == "x ":
            self.raw = "x " + new_priority + self.raw[2:]
        else:
            self.raw = new_priority + self.raw
        self.update(self.raw)
```
