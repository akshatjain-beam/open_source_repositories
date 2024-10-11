import unittest
import datetime
from todd.tasklib import Task, Util  # Adjust import as necessary based on your module structure

class TestTaskSetDone(unittest.TestCase):
    """Unit tests for the Task class's set_done method."""

    def setUp(self):
        """Set up a new Task instance for testing."""
        self.task_id = 1
        self.task = Task("Sample task", self.task_id)

    def test_mark_done_when_not_done(self):
        """Test that marking a task as done updates its status correctly.
        
        When a task is initially not done and is marked done, 
        the task's status should reflect that it is done, 
        and the raw text should start with 'x ' followed by today's date.
        """
        self.task.set_done(True)
        self.assertTrue(self.task.is_done())
        self.assertTrue(self.task.raw.startswith("x "))
        self.assertIn(datetime.date.today().isoformat(), self.task.raw)

    def test_mark_done_when_already_done(self):
        """Test that marking a task as done again does not change the raw text.
        
        When a task is already marked done, calling set_done(True) again
        should not modify the task's raw text.
        """
        self.task.set_done(True)  # Mark it done
        initial_raw = self.task.raw  # Store the initial raw value
        self.task.set_done(True)  # Attempt to mark it done again
        self.assertEqual(self.task.raw, initial_raw)  # Raw should not change

    def test_mark_not_done_when_done(self):
        """Test that marking a task as not done updates its status correctly.
        
        When a task is marked done and then marked not done, 
        the task's status should reflect that it is no longer done,
        and the raw text should not contain 'x '.
        """
        self.task.set_done(True)  # Mark it done
        self.task.set_done(False)  # Now mark it not done
        self.assertFalse(self.task.is_done())
        self.assertNotIn("x ", self.task.raw)

    def test_set_done_does_not_change_when_done(self):
        """Test that calling set_done(True) does not change the task when it's already done.
        
        When a task is already marked done, calling set_done(True) 
        should maintain the same raw text without any changes.
        """
        self.task.set_done(True)  # Mark it done
        previous_raw = self.task.raw
        self.task.set_done(True)  # Mark it done again
        self.assertEqual(self.task.raw, previous_raw)

    def test_raw_text_after_setting_done(self):
        """Test that the raw text is updated correctly when marking a task as done.
        
        After marking a task as done, the raw text should start with 'x ' 
        and include today's date.
        """
        self.task.update("Sample task")
        self.task.set_done(True)
        self.assertTrue(self.task.raw.startswith("x "))
        self.assertIn(datetime.date.today().isoformat(), self.task.raw)

    def test_raw_text_after_unsetting_done(self):
        """Test that the raw text is updated correctly when unmarking a task as done.
        
        After marking a task as done, when it is then marked not done,
        the raw text should not contain 'x '.
        """
        self.task.update("x 2024-10-10 Sample task")
        self.task.set_done(False)
        self.assertNotIn("x ", self.task.raw)
    

if __name__ == "__main__":
    unittest.main()
