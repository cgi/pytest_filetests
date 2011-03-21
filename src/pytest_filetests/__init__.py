import pytest
#  Origin version of file was taken from:
#     http://pytest.org/example/nonpython.html#non-python-tests
#
#

def pytest_collect_file(path, parent):
    if path.ext == ".yml" and path.basename.startswith("test"):
        return YamlFile(path, parent)
            
class YamlFile(pytest.File):
    def collect(self):
        import yaml # we need a yaml parser, e.g. PyYAML
        raw = yaml.load(self.fspath.open())
        for tc_name, tc_spec in raw.items():
            yield YamlItem(tc_name, self, tc_spec)

class YamlItem(pytest.Item):
    def __init__(self, name, parent, spec):
        super(YamlItem, self).__init__(name, parent)
        self.spec = spec
    
    def runtest(self):
       # !!!TODO: test code
        for name, value in self.spec.items():
            # some custom test execution (dumb example follows)
            if name != value:
                raise YamlException(self, name, value)

    def repr_failure(self, excinfo):
        """ called when self.runtest() raises an exception. """
        if isinstance(excinfo.value, YamlException):
            return "\n".join([
                "usecase execution failed",
                "   spec failed: %r: %r" % excinfo.value.args[1:3],
                "   no further details known at this point."
            ])

    def reportinfo(self):
        return self.fspath, 0, "usecase: {}".format( self.name )

class YamlException(Exception):
    """ custom exception for error reporting. """

