from TestHelperSuperClass import testHelperSuperClass
from executor import executeCommand

#kong_test is a script that queries kong and returns it's version number
## To test kong is running and active

class test_kong_test(testHelperSuperClass):
  def test_noArgs(self):

    expectedOutput = "Start of ./scripts/kong_test\nWrong number of arguments expected 1 - got 0\nRecieved args:\n['./scripts/kong_test']\n-\n"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/kong_test"

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1, False)

  def test_badKongServer(self):

    cmdToExecute = "./scripts/kong_test http://126.55.12.1:8001"
    expectedOutput = None
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [-1], 0.5, False)

  def test_WorkingKongServer(self):

    cmdToExecute = "./scripts/kong_test " + self.kong_server
    expectedOutput = "Start of ./scripts/kong_test\n"
    expectedOutput += " testing " + self.kong_server + "\n"
    expectedOutput += "Kong version: " + self.expected_kong_version + "\n"
    expectedOutput += "End of ./scripts/kong_test\n"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 2, False)

  def test_commandExeuteTimeout(self):
    cmdToExecute = "sleep 10"
    expectedOutput = ""
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [-1], 2, True)
