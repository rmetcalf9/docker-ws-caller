from TestHelperSuperClass import testHelperSuperClass
from executor import executeCommand
import time

class local_helpers(testHelperSuperClass):
  def delete_all_upstreams(self):
    resp, respCode = self.callKongService("/upstreams", {}, "get", None, [200])
    for x in resp["data"]:
      #print("x", x)
      resp, respCode = self.callKongService("/upstreams/" + x["id"], {}, "delete", None, [204])
    time.sleep(0.3)
    return
    
  def add_new_upstream(self, serviceName, targetName, removeOtherTargets):
    #executes code under test
    removeOtherTargetsString = "null"
    if removeOtherTargets:
      removeOtherTargetsString = "remove_other_targets"
    cmdToExecute = "./scripts/kong_add_upstream " + self.kong_server + " " + serviceName + " " + targetName + " " + removeOtherTargetsString

    expectedOutput = "Start of ./scripts/kong_add_upstream\nWrong number of arguments expected 4 - got 0\nRecieved args:\n['./scripts/kong_add_upstream']\n-"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, True)
    outputLines = a.stdout.decode().strip().strip("\n").split("\n")
    self.assertEqual(len(outputLines),10, msg="Wrong number of lines in output")
    self.assertEqual(outputLines[0], "Start of ./scripts/kong_add_upstream", msg="Error in line 1")
    self.assertEqual(outputLines[1], "Will remove other targets", msg="Error in line 2")
    self.assertEqual(outputLines[2], " Add (or update) upstream " + serviceName + " with target " + targetName + " " + self.kong_server, msg="Error in line 3")
    self.assertEqual(outputLines[3], "", msg="Error in line 4")
    self.assertEqual(outputLines[4], "", msg="Error in line 5")
    self.assertEqual(outputLines[5], "", msg="Error in line 6")
    self.assertEqual(outputLines[6], "", msg="Error in line 7")
    self.assertEqual(outputLines[7], "", msg="Error in line 8")
    self.assertEqual(outputLines[8], "", msg="Error in line 9")
    self.assertEqual(outputLines[9], "", msg="Error in line 10")
    self.assertTrue(False)

    return
  
class test_kong_test(local_helpers):
  def test_noArgs(self):
    expectedOutput = "Start of ./scripts/kong_add_upstream\nWrong number of arguments expected 4 - got 0\nRecieved args:\n['./scripts/kong_add_upstream']\n-"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/kong_add_upstream"

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1, False)


  def test_add_completly_new_upstream(self):
    self.delete_all_upstreams()
    self.add_new_upstream("service_name", "target_Name", True)
    #get_upstream_target_list
    #assert_target_matches
    #assert_upstream_has_single_target
  
    pass
  def test_add_existing_new_upstream_to_same_target(self):
    #delete_all_upstreams
    #add_new_upstream
    #add_new_upstream_with_same_target
    #get_upstream_target_list
    #assert_target_matches
    #assert_upstream_has_single_target
    pass

  def test_add_existing_upstream_and_remove_other_targets(self):
    #delete_all_upstreams
    #add_new_upstream
    #add_same_upstream_with_different_target
    #get_upstream_target_list
    #assert_target_matches_new_value
    #assert_upstream_has_single_target

    pass
  def test_add_existing_upstream_and_donot_remove_other_targets(self):
    #delete_all_upstreams
    #add_new_upstream
    #add_same_upstream_with_different_target
    #get_upstream_target_list
    #assert_target_matches_new_value
    #assert_upstream_has_two_targets
    pass


