from TestHelperSuperClass import testHelperSuperClass
from executor import executeCommand
import python_Testing_Utilities


scriptName="docker_service_remove_non_live"

class local_helpers(testHelperSuperClass):
  pass

class test_kong_test(local_helpers):
  def test_noArgs(self):
    expectedOutput = "Start of ./scripts/" + scriptName + "\n"
    expectedOutput += "Wrong number of arguments expected 3 - got 0\n"
    expectedOutput += "Recieved args:\n"
    expectedOutput += "['./scripts/docker_service_remove_non_live']\n"
    expectedOutput += "Expecting:\n"
    expectedOutput += "Arg 1: WS_NAME (Used to derive service name - saas_user_management_system)\n"
    expectedOutput += "Arg 2: VERSION  (Must be 3 . seperated numbers - 0.0.1)\n"
    expectedOutput += "Arg 3: IMAGE_PREFIX (e.g. dockerhub user - metcarob/)\n"
    expectedOutput += "-\n"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/" + scriptName

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1, False)

  def test_noservicerunning(self):
    ws_name = "xx"
    version = "0.4.5"
    image_prefix = "metcarob/"
    expectedOutput = "Start of ./scripts/" + scriptName + "\n"
    expectedOutput += "Given a service name and version stops all services and removes all images that don't match that version\n"
    expectedOutput += "ws_name:" + ws_name + "\n"
    expectedOutput += "version:" + version + "\n"
    expectedOutput += "image_prefix:" + image_prefix + "\n"
    expectedOutput += "End of ./scripts/" + scriptName + "\n"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/" + scriptName + " " + ws_name + " " + version + " " + image_prefix

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, False)
