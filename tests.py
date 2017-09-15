import unittest
from server import SimpleChatServer
from client import SimpleChatUser

class LoginChatTest(unittest.TestCase):
    def setUp(self):
        self.server = SimpleChatServer()
        self.server.start()
        self.alice = SimpleChatUser()
        self.alice2 = SimpleChatUser()

    def runTest(self):
        # simple login
        response = self.alice.login("Alice")
        self.assertTrue(response.startswith("Welcome to chat Alice, type 'exit' for leaving from chat"))

        # login with used nick
        response = self.alice2.login("Alice")
        self.assertTrue(response == "Fail_Nick")

    def tearDown(self):
        self.alice.exit()
        self.server.stop()


if __name__ == '__main__':
    unittest.main()