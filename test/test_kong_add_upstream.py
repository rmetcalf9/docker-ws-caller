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
  
  def get_upstream_targetlist(self, serviceName):
    resp, respCode = self.callKongService("/upstreams/" + serviceName + "/targets", {}, "get", None, [200])
    return resp["data"]
  
  def add_new_upstream(self, serviceName, targetName, removeOtherTargets, expectUpstreamToExist):
    #executes code under test
    removeOtherTargetsString = "null"
    if removeOtherTargets:
      removeOtherTargetsString = "remove_other_targets"
    cmdToExecute = "./scripts/kong_add_upstream " + self.kong_server + " " + serviceName + " " + targetName + " " + removeOtherTargetsString

    expectedOutput = "Start of ./scripts/kong_add_upstream\nWrong number of arguments expected 4 - got 0\nRecieved args:\n['./scripts/kong_add_upstream']\n-"
    expectedErrorOutput = None

    expectedLinesInOutput = 10
    if expectUpstreamToExist:
      expectedLinesInOutput = expectedLinesInOutput - 1

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, True)
    outputLines = a.stdout.decode().strip().strip("\n").split("\n")
    self.assertEqual(len(outputLines),expectedLinesInOutput, msg="Wrong number of lines in output")
    
    compline = 0
    self.assertEqual(outputLines[compline], "Start of ./scripts/kong_add_upstream", msg="Error in line " + str(compline+1))
    compline += 1
    self.assertEqual(outputLines[compline], "Will remove other targets", msg="Error in line " + str(compline+1))
    compline += 1
    self.assertEqual(outputLines[compline], " Add (or update) upstream " + serviceName + " with target " + targetName + " " + self.kong_server, msg="Error in line " + str(compline+1))
    
    if not expectUpstreamToExist:
      compline += 1
      self.assertEqual(outputLines[compline], "Upstream dosen't already exist - Creating", msg="Error in line " + str(compline+1))

    compline += 1
    self.assertEqual(outputLines[compline], "Adding target to upstream", msg="Error in line " + str(compline+1))
    compline += 1
    #self.assertEqual(outputLines[5], "Target ID:dfe001ec-8ce2-438e-9793-71a694aaea35", msg="Error in line 6")
    compline += 1
    self.assertEqual(outputLines[compline], "Now removing all other targets", msg="Error in line " + str(compline+1))
    compline += 1
    self.assertEqual(outputLines[compline], "Not removing - current target", msg="Error in line " + str(compline+1))
    compline += 1
    self.assertEqual(outputLines[compline], "Number of targets removed: 0", msg="Error in line " + str(compline+1))
    compline += 1
    self.assertEqual(outputLines[compline], "End of ./scripts/kong_add_upstream", msg="Error in line " + str(compline+1))

    return
  
class test_kong_test(local_helpers):
  def test_noArgs(self):
    expectedOutput = "Start of ./scripts/kong_add_upstream\nWrong number of arguments expected 4 - got 0\nRecieved args:\n['./scripts/kong_add_upstream']\n-"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/kong_add_upstream"

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1, False)


  def test_add_completly_new_upstream(self):
    test_service_name = "service_name"
    test_target_name1 = "target_Name:8022"
    self.delete_all_upstreams()
    self.add_new_upstream(test_service_name, test_target_name1, True, expectUpstreamToExist=False)
    upstreamTargets = self.get_upstream_targetlist(test_service_name)
    self.assertEqual(len(upstreamTargets), 1, msg="Wrong number of targets")
    self.assertEqual(upstreamTargets[0]["target"],test_target_name1, msg="Target mismatch")
  
    pass
  def test_add_existing_new_upstream_to_same_target(self):
    test_service_name = "service_name"
    test_target_name1 = "target_Name:8022"
    self.delete_all_upstreams()
    self.add_new_upstream(test_service_name, test_target_name1, True, expectUpstreamToExist=False)
    self.add_new_upstream(test_service_name, test_target_name1, True, expectUpstreamToExist=True)
    upstreamTargets = self.get_upstream_targetlist(test_service_name)
    self.assertEqual(len(upstreamTargets), 1, msg="Wrong number of targets")
    self.assertEqual(upstreamTargets[0]["target"],test_target_name1, msg="Target mismatch")

  def test_add_existing_upstream_and_remove_other_targets(self):
    test_service_name = "service_name"
    test_target_name1 = "target_Name:8022"
    test_target_name2 = "target_Name2:8022"
    self.delete_all_upstreams()
    self.add_new_upstream(test_service_name, test_target_name1, True, expectUpstreamToExist=False)
    self.add_new_upstream(test_service_name, test_target_name2, True, expectUpstreamToExist=True)
    upstreamTargets = self.get_upstream_targetlist(test_service_name)
    self.assertEqual(len(upstreamTargets), 1, msg="Wrong number of targets")
    self.assertEqual(upstreamTargets[0]["target"],test_target_name1, msg="Target mismatch")

    pass
  def test_add_existing_upstream_and_donot_remove_other_targets(self):
    #delete_all_upstreams
    #add_new_upstream
    #add_same_upstream_with_different_target
    #get_upstream_target_list
    #assert_target_matches_new_value
    #assert_upstream_has_two_targets
    pass


