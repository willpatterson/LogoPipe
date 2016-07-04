import unittest

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
        assert(batches[0].name)
        assert(isinstance(batches[0].inputs, list))
        assert(isinstance(addresses, list))
        assert(addresses[0] == 'wpatt2@pdx.edu')

class TestBatch(unittest.TestCase):
    """Test Class for Batch"""

    def test__new__factory(self):
        ssh_params = {'batch_type': 'ssh', 'command': 'test'}
        slurm_params = {'batch_type': 'slurm', 'command': 'test'}
        local_params = {'batch_type': 'local', 'command': 'test'}
        typeless_params = {'command': 'test'}
        assert(isinstance(Batch(**ssh_params), SshBatch))
        assert(isinstance(Batch(**slurm_params), SlurmBatch))
        assert(isinstance(Batch(**local_params), LocalBatch))
        assert(isinstance(Batch(**typeless_params), LocalBatch))

    """
    def test_format_command(self):
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

