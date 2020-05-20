from os.path import dirname, join
from unittest import TestCase
from pytezos import ContractInterface, MichelsonRuntimeError

# run this test with :
# pytest test.py


class TestContractTest(TestCase):

    @classmethod
    def setUpClass(cls):
        project_dir = dirname(dirname(__file__))
        print("projectdir", project_dir)
        cls.test = ContractInterface.create_from(
            join(project_dir, 'src/vote.tz'))

    def test_vote_1(self):
        u = "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z"
        res = 1
        result = self.test.vote(
            1
        ).result(
            storage={
                "status": True,
                "yes": 0,
                "no": 0,
                "voters": set()
            },
            sender = u
        )
        self.assertEqual(res, result.storage["yes"])

    def test_vote_2(self):
        u = "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z"
        res = 1
        result = self.test.vote(
            2
        ).result(
            storage={
                "status": True,
                "yes": 0,
                "no": 0,
                "voters": set()
            },
            sender = u
        )
        self.assertEqual(res, result.storage["no"])

    def test_vote_3(self):
        owner = "tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx"
        res = 1
        with self.assertRaises(MichelsonRuntimeError):
            result = self.test.vote(
                1
            ).result(
                storage={
                    "status": True,
                    "yes": 0,
                    "no": 0,
                    "voters": set()
                },
                sender = owner
            )

    def test_vote_4(self):
        u = "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z"
        res = 1
        with self.assertRaises(MichelsonRuntimeError):
            result = self.test.vote(
                1
            ).result(
                storage={
                    "status": False,
                    "yes": 0,
                    "no": 0,
                    "voters": set()
                },
                sender = u
            )


    def test_reset_1(self):
        owner = "tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx"
        result = self.test.reset(69).result(
            storage={
                "status": False,
                "yes": 4,
                "no": 6,
                "voters": set()
            },
            sender = owner
        )
        self.assertEqual(0, result.storage["yes"])

    def test_reset_2(self):
        owner = "tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx"

        with self.assertRaises(MichelsonRuntimeError):
            result = self.test.reset(69).result(
                storage={
                    "status": True,
                    "yes": 0,
                    "no": 0,
                    "voters": set()
                },
                sender = owner
            )

    def test_reset_3(self):
        u = "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z"

        with self.assertRaises(MichelsonRuntimeError):
            result = self.test.reset(69).result(
                storage={
                    "status": True,
                    "yes": 0,
                    "no": 0,
                    "voters": set()
                },
                sender = u
            )


    def test_stdby_1(self):
        owner = "tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx"
        res = False
        result = self.test.pause("False").result(
                storage={
                    "status":True,
                    "yes":0,
                    "no":0,
                    "voters":set()
                },
                sender = owner
        )
        self.assertEqual(res, result.storage["yes"])
    
    def test_stdby_2(self):
        owner = "tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx"
        res = True
        result = self.test.pause("True").result(
                storage={
                    "status":False,
                    "yes":0,
                    "no":0,
                    "voters":set()
                },
                sender = owner
        )
        self.assertEqual(res, result.storage["status"])

