import py
import pytest
import re
#  Origin version of file was taken from:
#     http://pytest.org/example/nonpython.html#non-python-tests
#
#

def pytest_collect_file(path, parent):
    if path.ext in (".yml", ".yaml") and path.basename.startswith("test"):
        return YamlFile(path, parent)
            
class YamlFile(pytest.File):
    def collect(self):
        import yaml # we need a yaml parser, e.g. PyYAML
        raw = yaml.load( open( str(self.fspath), encoding='utf-8') )
        for tc_name, tc_spec in raw.items():
            yield YamlItem(tc_name, self, tc_spec)

class YamlItem(pytest.Item):
    def __init__(self, name, parent, spec):
        super(YamlItem, self).__init__(name, parent)
        self.spec = spec
        self.description = spec.get('test_desc', '')
    
    def runtest(self):
        for name, value in self.spec.items():
            # some custom test execution (dumb example follows)
            if name in ('test_desc'):
               pass   
            elif name in ('assert_file_exists'):
               FileExistsItem(**value).test()   
            else:
               raise TestFileException(self, 0, name, value )

    def repr_failure(self, excinfo):
        """ called when self.runtest() raises an exception. """

        if isinstance(excinfo.value, TestFileException):
            return "\n".join([
                "Тест проведен:",
                "   результат: {}".format( excinfo.value.find_count ),
                "   условие: {}".format( excinfo.value.condition ),
                "   дополнительная информация: {}".format(excinfo.value.ext_info)
            ])
        else:
            super(YamlItem, self).repr_failure(excinfo)

    def reportinfo(self):
        return self.fspath, 0, "usecase: {0} ({1})".format( self.name, self.description )

class FileExistsItem(object):
    def __init__(self, file_mask, file_count_eval=None):
        super(FileExistsItem, self).__init__()
        if file_count_eval is None:
           file_count_eval = 'count > 0'
        self.file_re = re.compile(file_mask, re.IGNORECASE)
        self.file_count_eval = file_count_eval
 
    def test(self):
        start_path = py.path.local('.')
        files = [p.relto(start_path) for p in start_path.visit()]
        matches = [p for p in files if self.file_re.search(p) ]
        count = len(matches)
        res = eval(self.file_count_eval, {'count':count}, dict())
        if not res:
           raise TestFileException(self, count, self.file_count_eval, matches)
 
class TestFileException(Exception):
    """ Исключение, для обработки и показа ошибок, связанных с поиском файлов """
    def __init__(self, find_count, condition, ext_info):
        super(TestFileException, self).__init__()
        self.find_count = find_count
        self.condition = condition
        self.ext_info = ext_info

