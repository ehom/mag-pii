import time
import helper as Helper

def timing_decorator(f):
    def wrapper(*args):
        time1 = time.time()
        return_value = f(*args)
        time2 = time.time()
        s = '{:s} function took {:.3f} ms'
        print(s.format(f.__name__, (time2-time1)*1000.0))
        print("# of repos recorded: {}".format(len(return_value)))
        return return_value
    return wrapper


def show_progress(f):
    def wrapper(owner, input):
        repos = f(owner, input)
        print("Retrieved {} more repos...".format(len(repos['nodes'])))
        return repos
    return wrapper


def save_as_json_hash_table(f):
    def wrapper(obj, filepath):
        f(obj, filepath)
        filepath = "table-of-" + filepath
        Helper.save_as_json_hash_table(obj, filepath)
        print("Generated \"{}\".".format(filepath))
    return wrapper


def save_as_json(f):
    def wrapper(obj, filepath):
        f(obj, filepath)
        Helper.save_as_json(obj, filepath)
        print("Generated \"{}\".".format(filepath))
    return wrapper
