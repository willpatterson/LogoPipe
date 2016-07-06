import unittest
import os

from logobatch.batches import Batch, SshBatch, SlurmBatch, LocalBatch
from logobatch.logobatch import BatchManager

BATCH_BASE = "test/test_batch_base"
BBATCH = "test/t_bbatch.yml"

class TestBatchManager(unittest.TestCase):
    """ Test Class for BatchManager"""

    def setUp(self):
        self.bm = BatchManager(BBATCH, BATCH_BASE)

    def test_parse_bbatch(self):
        """tests parse_bbatch method"""
        batches, addresses = self.bm.parse_bbatch(BBATCH)
        assert(isinstance(batches, list))
        assert(isinstance(batches[0], SshBatch))
        assert(isinstance(batches[1], SlurmBatch))
        assert(batches[0].name == 'sshb')
        assert(isinstance(batches[0].inputs, list))
        assert(isinstance(addresses, list))
        assert(addresses[0] == 'wpatt2@pdx.edu')

TEST_CSV = 'test/input_test.csv'
TEST_SINGLE_FILE = 'test/t_bbatch.yml'
TEST_DIR = 'test/input_dir_test'

class TestBatch(unittest.TestCase):
    """Test Class for Batch"""

    def test__new__factory(self):
        ssh_params = {'batch_type': 'ssh',
                      'hostnames': ['test.local'],
                      'command': 'test'}
        slurm_params = {'batch_type': 'slurm',
                        'command': 'test'}
        local_params = {'batch_type': 'local',
                        'command': 'test'}
        typeless_params = {'command': 'test'}
        assert(isinstance(Batch(**ssh_params), SshBatch))
        assert(isinstance(Batch(**slurm_params), SlurmBatch))
        assert(isinstance(Batch(**local_params), LocalBatch))
        assert(isinstance(Batch(**typeless_params), LocalBatch))

    def test_generate_inputs(self):
        """tests three outcomes of the generate inputs static method"""

        #CSV input parsing
        split_csv = [x for x in Batch.generate_inputs(TEST_CSV)]
        assert(split_csv == [{'1','2','3','4'},{'a','b','c','df'}])

        #Single file path yield
        file_path = [x for x in Batch.generate_inputs(TEST_SINGLE_FILE)]
        assert(file_path == [os.path.realpath(TEST_SINGLE_FILE)])

        #Direcotry file yield
        dir_list = [x for x in Batch.generate_inputs(TEST_DIR)]
        assert(dir_list == [os.path.realpath(os.path.join(TEST_DIR, 't1')),
                            os.path.realpath(os.path.join(TEST_DIR, 't2')),
                            os.path.realpath(os.path.join(TEST_DIR, 't3'))])

    def test_format_command(self):
        """
        Tests format_command
        TODO tests:
            CSV input markers
            class attribute and CSV input markers
            execeptions and warnings
        """

        #Test class attribute input markers
        class_attr_params = {'batch_type': 'ssh',
                             'hostnames': ['test.local'],
                             'command': '{batch_base} {name}'}
        sshb = Batch(**class_attr_params)
        command = sshb.format_command(1)
        assert(command == '{} {}'.format(sshb.batch_base, sshb.name))

        """
        #Test CSV input markers
        sshb.command_base = 'ID: {i} {i0} {i1} {i2} {i3}'
        command = sshb.format_command(1, inputs={'0','1','2','3'})
        print(command)
        assert(command == '1 0 1 2 3')
        """

class TestSshBatch(unittest.TestCase):
    """ """
    def setUp(self):
        bm = BatchManager(BBATCH, BATCH_BASE)
        self.ssh_batch = bm.batches[0]

class TestSlurmBatch(unittest.TestCase):
    """ """
    def setUp(self):
        bm = BatchManager(BBATCH, BATCH_BASE)
        self.slurm_batch = bm.batches[1]

if __name__ == '__main__':
    test_classes = (TestBatch, TestBatchManager)
    test_suite = unittest.TestSuite()
    for test_class in test_classes:
        test_suite.addTest(test_class())

    runner = unittest.TextTestRunner()
    runner.run(test_suite)

