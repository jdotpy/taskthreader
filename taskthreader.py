import threading
import time

class Worker(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.target = kwargs['target']
        self.args = kwargs['args']
        self.kwargs = kwargs['kwargs']
        super(Worker, self).__init__(*args, **kwargs)

    def run(self):
        try:
            self.result = self.target(*self.args, **self.kwargs)
        except Exception as e:
            self.result = e

class WorkGroup():
    def __init__(self, max_threads=5, tasks=None):
        self.max_threads = max_threads

        self.tasks = {}
        tasks = tasks or {}
        for name, task in tasks.items():
            args = (name,) + task
            self._add_task(*args)

    def add_task(self, name, func, *args, **kwargs):
        """ This method just wraps the internal one collapsing the args and kwargs """
        self._add_task(name, func, args, kwargs)

    def _add_task(self, name, func, args=None, kwargs=None):
        self.tasks[name] = (func, args, kwargs)

    def run(self, tasks=None):
        start_time = time.time()
        results = {}
        tasks = tasks or self.tasks

        task_queue = [(task_name, ) + task for task_name, task in tasks.items()]

        # Start threads for them 
        active_workers = set()

        while True:
            # Clean up complete workers
            for worker in list(active_workers):
                if not worker.is_alive():
                    results[worker.name] = worker.result
                    active_workers.remove(worker)

            # Finish if work is done
            if len(task_queue) == 0 and len(active_workers) == 0:
                break

            # If we have open worker slots available use them
            to_make = self.max_threads - len(active_workers) 
            to_make = min(to_make, len(task_queue))
            if to_make:
                for i in range(to_make):
                    name, func, args, kwargs = task_queue.pop()
                    new_worker = Worker(
                        name=name,
                        target=func,
                        args=args,
                        kwargs=kwargs
                    )
                    new_worker.daemon = True
                    active_workers.add(new_worker)
                    new_worker.start()

            # Wait on next thread to finish
            watched = active_workers.pop() # Instead of iterating over to grab an item, i'm popping and re-adding
            active_workers.add(watched)
            watched.join()
        end_time = time.time()
        self.last_run_time = end_time - start_time
        return results
