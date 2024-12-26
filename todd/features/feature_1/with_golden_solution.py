```
    def set_priority(self, new_priority):
        if self.priority == new_priority:
            return
        if new_priority:
            new_priority = "({}) ".format(new_priority)

        # Task
        if re.search(self._priority_regex, self.raw):
            self.raw = re.sub(self._priority_regex, "{}".format(new_priority), self.raw)
        elif re.search(r"^x \d{4}-\d{2}-\d{2}", self.raw):
            self.raw = re.sub(r"^(x \d{4}-\d{2}-\d{2}) ", r"\1 {}".format(new_priority), self.raw)
        else:
            self.raw = "{}{}".format(new_priority, self.raw)
        self.update(self.raw)
```