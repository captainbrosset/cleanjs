import imp, os

def load_from_file(filepath, expected_class):
    class_inst = None
    mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])
    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)
    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, filepath)
    if expected_class in dir(py_mod):
        class_inst = py_mod.Reviewer() 
    class_inst.set_name(mod_name)
    return class_inst