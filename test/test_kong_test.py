from TestHelperSuperClass import testHelperSuperClass
from executor import executeCommand

#kong_test is a script that queries kong and returns it's version number
## To test kong is running and active

class test_kong_test(testHelperSuperClass):
  def test_noArgs(self):

    expectedOutput = "Start of ./scripts/kong_test\nWrong number of arguments expected 1 - got 0\nRecieved args:\n['./scripts/kong_test']\n-\n"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/kong_test"
    
    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1)

  def test_badKongServer(self):

    cmdToExecute = "./scripts/kong_test http://126.55.12.1:8001"
    expectedOutput = None
    expectedErrorOutput = None
    
    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [-1], 0.5)

  def test_WorkingKongServer(self):

    cmdToExecute = "./scripts/kong_test http://127.0.0.1:8381"
    expectedOutput = "Start of ./scripts/kong_test\n testing http://127.0.0.1:8381\nKong version0.13.1\nEnd of ./scripts/kong_test\n"
    expectedErrorOutput = None
    
    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 2)


