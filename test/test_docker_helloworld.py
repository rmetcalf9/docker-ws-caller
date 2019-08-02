from TestHelperSuperClass import testHelperSuperClass
from executor import executeCommand
import python_Testing_Utilities


scriptName="docker_helloworld"

class local_helpers(testHelperSuperClass):
  pass

class test_kong_test(local_helpers):
  def test_noArgs(self):
    expectedOutput = "Start of ./scripts/" + scriptName + "\n"
    expectedOutput += "Checks docker is working by listing containers\n"
    expectedOutput += "LOTSOFLINES\n"
    expectedOutput += "End of ./scripts/" + scriptName + "\n"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/" + scriptName

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, True)
    outputLines = a.stdout.decode().strip().strip("\n").split("\n")
    expectedLines = expectedOutput.strip().strip("\n").split("\n")

    self.assertEqual(outputLines[0],expectedLines[0])
    self.assertEqual(outputLines[1],expectedLines[1])

    self.assertEqual(outputLines[len(outputLines)-1],expectedLines[3])
