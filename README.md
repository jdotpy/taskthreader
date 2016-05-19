# TaskThreader
 
**Description**: 

This package provides a way to run different tasks in parallel using threads and then access their results by name

  - **Technology stack**: Python
  - **Status**: Beta
 
## Dependencies

  - Python 2.7+ or 3.3+
 
## Installation

	pip install <github version of your choice>
 
## Usage

	>>> from taskthreader import WorkGroup
	>>> import time
	>>>
    >>> def example_task(result, wait_time=.1):
    >>>     time.sleep(wait_time)
    >>>     return result
	>>>
	>>> work_group = WorkGroup(max_threads=2)
    >>> work_group.add_task('foo', task, 1)
    >>> work_group.add_task('bar', task, 2)
    >>> work_group.add_task('zip', task, 3)
	>>>
	>>> results = work_group.run()
	>>> results
	{"foo": 1, "bar": 2, "zip": 3}

## How to test the software
 
* Clone/download project.
* Create new virtualenv
* Install requirements
	pip install -r requirements.txt
	./run_tests.sh
 
## Known issues

* None atm
 
## Getting help

https://github.com/jdotpy/taskthreader
