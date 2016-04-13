#!/usr/bin/env python

import os

from doit.tools import run_once, create_folder, title_with_actions, LongRunning
from doit.tools import PythonInteractiveAction
from doit.task import clean_targets, dict_to_task
from doit.cmd_base import TaskLoader
from doit.doit_cmd import DoitMain


def create_doit_task(task_dict_func):
    '''Wrapper to decorate functions returning pydoit
    Task dictionaries and have them return pydoit Task
    objects
    '''
    def d_to_t(*args, **kwargs):
        ret_dict = task_dict_func(*args, **kwargs)
        return dict_to_task(ret_dict)
    return d_to_t


def task_str(task):
    return '{{ Task: {0}\n  actions: {1}\n  file_dep: {2}'\
           '\n  task_dep: {3}\n  targets: {4} }}'.format(task.name, task.actions,
                                                         task.file_dep, task.task_dep,
                                                         task.targets)


def run_tasks(tasks, args, config={'verbosity': 2}):
   
    tasks = list(tasks)

    class Loader(TaskLoader):
        @staticmethod
        def load_tasks(cmd, opt_values, pos_args):
            return tasks, config
   
    return DoitMain(Loader()).run(args)

class ShortenedPythonAction(PythonInteractiveAction):

    def __str__(self):
        fullname = str(self.py_callable)[1:].split(' at ')[0]
        _, _, shortname = fullname.rpartition('.')
        return "Python: %s" % shortname

class DependencyError(RuntimeError):
    pass


def which(program, raise_err=True):
    '''Checks whether the given program (or program path) is valid and
    executable.

    NOTE: Sometimes copypasta is okay! This function came from stackoverflow:

        http://stackoverflow.com/a/377028/5109965

    Args:
        program (str): Either a program name or full path to a program.

    Returns:
        Return the path to the executable or None if not found
    '''
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    if raise_err:
        raise DependencyError('{0} not found; is it installed?'.format(program))
    else:
        return None


