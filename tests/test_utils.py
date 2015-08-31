#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os
import os.path
import unittest
from simiki import utils

TEST_PATH = os.path.join(os.path.dirname(__file__), 'mywiki_for_others')

class TestUtils(unittest.TestCase):

    def setUp(self):
        os.chdir(TEST_PATH)
        self.content = 'content'
        self.output = 'output'
        if os.path.exists(self.output):
            utils.emptytree(self.output)
            os.rmdir(self.output)

    def test_check_extension(self):
        valid_files = ['/tmp/file1.md', '/tmp/file2.mkd', '/tmp/文件3.mdown',
                       '/tmp/文件4.markdown', '/tmp/目录/文件5.md']
        for f in valid_files:
            assert utils.check_extension(f)

        invalid_files = ['/tmp/file6.txt', '/tmp/目录/文件7.mkdown']
        for f in invalid_files:
            assert not utils.check_extension(f)

    def test_copytree_common(self):
        utils.copytree(self.content, self.output)
        assert os.path.exists(self.output) and os.path.isdir(self.output)

        files = [
            os.path.join('python', 'zen_of_python.md'),
            os.path.join('python', 'python文档.md'),
            os.path.join('其它', 'helloworld.markdown'),
            os.path.join('其它', '维基.md'),
            os.path.join('其它', 'hello.txt'),
            os.path.join('其它', '.hidden.md'),
        ]
        for f in files:
            assert os.path.exists(os.path.join(self.output, f))

    def test_copytree_symlink(self):
        '''temp not support'''
        pass

    def test_copytree_ignore(self):
        '''temp not support'''
        pass

    def test_emptytree(self):
        utils.copytree(self.content, self.output)
        utils.emptytree(self.output)
        assert not os.listdir(self.output)

    def test_mkdir_p(self):
        path = os.path.join(self.content)
        utils.mkdir_p(path)
        assert os.path.exists(path)

        path = os.path.join(self.output, "dir1/dir2/dir3")
        utils.mkdir_p(path)
        assert os.path.exists(path)

        # test path exist, and not a directory
        path = os.path.join(self.content, '其它', 'hello.txt')
        self.assertRaises(OSError, lambda: utils.mkdir_p(path))

    def test_listdir_nohidden(self):
        fs = utils.listdir_nohidden(os.path.join(self.content, '其它'))
        expected_listdir = ['hello.txt', 'helloworld.markdown', '维基.md']
        assert sorted(list(fs)) == sorted(expected_listdir)

    def tearDown(self):
        if os.path.exists(self.output):
            utils.emptytree(self.output)
            os.rmdir(self.output)


if __name__ == '__main__':
    unittest.main()
