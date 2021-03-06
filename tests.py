import unittest
import time

from taskthreader import WorkGroup

def example_task(result=None, wait_time=.1, exc=None):
    if exc:
        raise exc()
    time.sleep(wait_time)
    return result

class WorkGroupTest(unittest.TestCase):
    work_time = .1

    def test_basic_work_group(self):
        # This funcgettion represents some work we want to accomplish

        # Run 3 tasks in parallel making sure their results are 
        # accurate and timing is less than if they ran in sequence
        work_group = WorkGroup()
        work_group.add_task('foo', example_task, 1, wait_time=self.work_time)
        work_group.add_task('bar', example_task, 2, wait_time=self.work_time)
        work_group.add_task('zip', example_task, 3, wait_time=self.work_time)
        success, results = work_group.run()
        assert success
        self.assertEqual(results['foo'], 1)
        self.assertEqual(results['bar'], 2)
        self.assertEqual(results['zip'], 3)
        self.assertTrue(work_group.last_run_time < self.work_time * 3)
    
        # Run again with threads set to one to run them in sequence
        work_group.max_threads = 1
        success2, results2 = work_group.run()
        assert success2
        self.assertTrue(work_group.last_run_time >= self.work_time * 3)

    def test_params(self):
        # Test the altnerate parameter style
        tasks = {
            'foo': (example_task, [1], {'wait_time': self.work_time}),
            'bar': (example_task, [2]),
            'zip': (example_task,)
        }
        work_group = WorkGroup(tasks=tasks)
        success, results = work_group.run()
        assert success
        self.assertEqual(results['foo'], 1)
        self.assertEqual(results['bar'], 2)
        self.assertEqual(results['zip'], None)

        work_group = WorkGroup()
        success, results = work_group.run(tasks=tasks)
        assert success
        self.assertEqual(results['foo'], 1)
        self.assertEqual(results['bar'], 2)

    def test_error(self):
        work_group = WorkGroup()
        work_group.add_task('foo', example_task, 1, wait_time=self.work_time)
        work_group.add_task('err', example_task, exc=KeyError)
        success, results = work_group.run()
        assert not success
        self.assertEqual(results['foo'], 1)
        assert isinstance(results['err'], KeyError)
