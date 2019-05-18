import unittest
from executor import executeCommand



class testHelperSuperClass(unittest.TestCase):
  def executeCommand(self, cmdToExecute, expectedOutput, expectedErrorOutput, expectedReturnCodes, timeout):

    commandOutputObj = executeCommand(cmdToExecute, timeout)
    
    correctReturnCode = False
    for x in expectedReturnCodes:
      if x == commandOutputObj.returncode:
        correctReturnCode = True
        
    def decode_or_none(v):
      if v is None:
        return None
      return v.decode()
    def bytes_to_string(v):
      if v is None:
        return None
      return str(v, "utf-8")
      
      
    if not correctReturnCode:
      print("stdOut:" + decode_or_none(commandOutputObj.stdout))
      print("stdErr:" + decode_or_none(commandOutputObj.stderr))
      self.assertFalse(True, msg="Wrong return code recieved got " + str(commandOutputObj.returncode) + " expected one of " + str(expectedReturnCodes))

    stdoutString = None
    stdoutString = bytes_to_string(commandOutputObj.stdout)
    stderrString = None
    stderrString = bytes_to_string(commandOutputObj.stderr)

    if stdoutString != expectedOutput:
      print("Wrong Output: GOT:")
      print(stdoutString)
      print("--------------EXP:")
      print(expectedOutput)
      print("--------------")
      self.assertTrue(False)

    self.assertEqual(stderrString,expectedErrorOutput,msg="Wrong Error Output")
    
    return commandOutputObj
