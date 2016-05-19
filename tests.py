import unittest
import time

from taskthreader import WorkGroup

class WorkGroupTest(unittest.TestCase):
    def test_work_group(self):
        # This function represents some work we want to accomplish
        work_time = .1
        def task(result, wait_time=work_time):
            time.sleep(wait_time)
            return result

        # Run 3 tasks in parallel making sure their results are 
        # accurate and timing is less than if they ran in sequence
        work_group = WorkGroup()
        work_group.add_task('foo', task, 1)
        work_group.add_task('bar', task, 2)
        work_group.add_task('zip', task, 3)
        results = work_group.run()
        self.assertEqual(results['foo'], 1)
        self.assertEqual(results['bar'], 2)
        self.assertEqual(results['zip'], 3)
        self.assertTrue(work_group.last_run_time < work_time * 3)
    
        # Run again with threads set to one to run them in sequence
        work_group.max_threads = 1
        results2 = work_group.run()
        self.assertTrue(work_group.last_run_time >= work_time * 3)
