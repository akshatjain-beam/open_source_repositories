import re
import datetime
from todd.tasklib import Util


class Task:
    """Task

    Format:
    x (A) 2000-01-01 2000-01-01 DESC

    DESC may contain
    - text
    - +TAG              tags
    - @CONTEXT          contexts
    - KEY:VALUE         special key-value tag

    Known key-value tags are
    - due:2000-01-01    due dates
    - rec:1y            recurring task
    """

    _priority_regex = re.compile(r"\(([A-Z])\) ")
    _context_regex = re.compile(r"(?:^|\s+)(@\S+)")
    _tag_regex = re.compile(r"(?:^|\s+)(\+\S+)")
    _done_regex = re.compile(r"^x (\d\d\d\d-\d\d-\d\d) ")
    _deleted_regex = re.compile(r"\s*del:(\S+)\s*")

    _creation_date_prefix = r"^" r"(x \d\d\d\d-\d\d-\d\d\s+)?" r"(\(\w\)\s+)?"
    _creation_date_regex = re.compile(_creation_date_prefix + r"(\d\d\d\d-\d\d-\d\d)\s*")
    _creation_date_regex2 = re.compile(_creation_date_prefix)

    _due_date_regex = re.compile(r"\s*due:(\d\d\d\d-\d\d-\d\d)\s*")
    _any_due_date_regex = re.compile(r"\s*due:(\S+)\s*")

    _rec_int_regex = re.compile(r"\s*rec:(\+?\d+[dwmy])\s*")
    _rec_int_parts_regex = re.compile(r"(\+)?(\d+)([dwmy])")

    PLHR = "\N{HORIZONTAL ELLIPSIS}"
    _plhr_regex = re.compile(PLHR + "[ " + PLHR + "]*")

    def __init__(self, item, task_id):
        self.task_id = task_id
        self.update(item)

    def update(self, text):
        self.raw = text.strip()
        self.priority = Task.scan_priority(self.raw)
        self.contexts = Task.scan_contexts(self.raw)
        self.tags = Task.scan_tags(self.raw)
        self.done_date = Task.scan_done_date(self.raw)
        self.creation_date = Task.scan_creation_date(self.raw)
        self.due_date = Task.scan_due_date(self.raw)
        self.rec_int = Task.scan_rec_int(self.raw)

    @staticmethod
    def scan_contexts(text):
        return sorted(Task._context_regex.findall(text))

    @staticmethod
    def scan_tags(text):
        return sorted(Task._tag_regex.findall(text))

    @staticmethod
    def scan_creation_date(text):
        match = Task._creation_date_regex.search(text)
        return match.group(3) if match else ""

    @staticmethod
    def scan_due_date(text):
        match = Task._due_date_regex.search(text)
        return match.group(1) if match else ""

    @staticmethod
    def scan_rec_int(text):
        match = Task._rec_int_regex.search(text)
        return match.group(1) if match else ""

    @staticmethod
    def scan_priority(text):
        match = Task._priority_regex.match(text)
        return match.group(1) if match else ""

    @staticmethod
    def scan_done_date(text):
        match = Task._done_regex.match(text)
        return match.group(1) if match else ""

    def __repr__(self):
        return repr(
            {
                "raw": self.raw,
                "task_id": self.task_id,
                "priority": self.priority,
                "done_date": self.done_date,
                "creation_date": self.creation_date,
                "contexts": self.contexts,
                "tags": self.tags,
                "due_date": self.due_date,
                "rec_int": self.rec_int,
            }
        )

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

    def is_done(self):
        return self.raw[0:2] == "x "

    def set_done(self, done=True):
        """
        Mark the task as done or undone and update its status accordingly.

        This method modifies the task's state based on the provided `done` parameter. If the task is already in the desired state, no action is taken.

        When marking the task as done:
        - The task's priority is removed.
        - The task's raw string is updated to include a completion marker (`x `), the current date in ISO format, and the existing raw string.
        - If the task has a recurrence interval, the due date is adjusted:
        - The recurrence interval is parsed into its prefix, value, and interval type using a regular expression `_rec_int_parts_regex`.
        - The prefix determines whether to add the recurrence interval to the current due date (if `prefix` is "+") or to today's date.
        - The new due date is calculated using the `date_add_interval` method from the `Util` class.

        When marking the task as undone, the completion marker is removed from the task's raw string using `_done_regex`.

        Args:
            done (bool): If True, marks the task as done; if False, marks it as undone.

        Returns:
            datetime or None: Returns the new due date if the task is marked as done and has a recurrence interval; otherwise, returns None.
        """
        $PlaceHolder$

    def is_deleted(self):
        match = Task._deleted_regex.search(self.raw)
        return match.group(1) == "true" if match else False

    def set_deleted(self, deleted=True):
        if self.is_deleted() == deleted:
            return
        match = Task._deleted_regex.search(self.raw)
        v = " del:true " if deleted else " "
        if match:
            text = re.sub(Task._deleted_regex, v, self.raw)
        else:
            text = self.raw + v
        self.update(text)

    def get_status(self, due_date, next_date=None):
        if self.is_done() or self.is_deleted():
            return ("done", 99999)
        if self.due_date:
            if self.due_date < due_date:
                return ("overdue", -1)
            elif self.due_date == due_date:
                return ("due", 0)
            elif self.due_date < next_date:
                return ("todo", 1)
            else:
                return ("todo", 2)
        return ("todo", 9999)

    def has_due(self):
        return self.due_date is not None

    def is_due(self, due_date):
        return not self.is_done() and self.due_date and self.due_date <= due_date

    def set_due(self, date):
        if type(date) is datetime.datetime:
            date = date.date()
        text = " due:" + date.isoformat()
        if self.due_date:
            self.raw = re.sub(Task._due_date_regex, text + " ", self.raw)
        else:
            self.raw += text
        self.update(self.raw)

    def get_due(self):
        return (
            datetime.datetime.strptime(self.due_date, "%Y-%m-%d").date() if self.due_date else None
        )

    def update_relative_due_date(self):
        if not Task.scan_due_date(self.raw):
            match = Task._any_due_date_regex.search(self.raw)
            if match:
                date = Util.mod_date_by(Util.get_today(), match.group(1))
                if date:
                    self.raw = re.sub(Task._any_due_date_regex, " ", self.raw).strip()
                    self.set_due(date)

    def set_creation_date(self, date):
        if type(date) is datetime.datetime:
            date = date.date()
        regex = (
            Task._creation_date_regex if self.creation_date != "" else Task._creation_date_regex2
        )
        self.raw = re.sub(regex, r"\g<1>\g<2>" + date.isoformat() + " ", self.raw)
        self.update(self.raw)

    def get_desc(self):
        PLHR = " \N{HORIZONTAL ELLIPSIS} "
        res = self.raw
        if self.creation_date != "":
            res = re.sub(Task._creation_date_regex, r"\1\2", res)
        res = re.sub(Task._due_date_regex, PLHR, res)
        res = re.sub(Task._rec_int_regex, PLHR, res)
        res = re.sub(Task._context_regex, PLHR, res)
        res = re.sub(Task._plhr_regex, PLHR, res)
        return res.strip(PLHR)
