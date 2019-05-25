from TestHelperSuperClass import testHelperSuperClass
from executor import executeCommand
import time
import copy

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
  
  def add_new_upstream(self, serviceName, targetName, removeOtherTargets, expectUpstreamToExist, targetsExpectedToBeRemoved):
    #executes code under test
    removeOtherTargetsString = "null"
    if removeOtherTargets:
      removeOtherTargetsString = "remove_other_targets"
    cmdToExecute = "./scripts/kong_add_upstream " + self.kong_server + " " + serviceName + " " + targetName + " " + removeOtherTargetsString

    expectedOutput = "Start of ./scripts/kong_add_upstream\nWrong number of arguments expected 4 - got 0\nRecieved args:\n['./scripts/kong_add_upstream']\n-"
    expectedErrorOutput = None

    expectedLinesInOutput = 7
    if expectUpstreamToExist:
      expectedLinesInOutput = expectedLinesInOutput - 1
    expectedLinesInOutput += len(targetsExpectedToBeRemoved)
    if removeOtherTargets:
      expectedLinesInOutput += 3

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, True)
    outputLines = a.stdout.decode().strip().strip("\n").split("\n")
    
    if len(outputLines) != expectedLinesInOutput:
      print("-----------Got Output len " + str(len(outputLines)) + "------------------")
      for x in outputLines:
        print(x)
      self.assertEqual(len(outputLines),expectedLinesInOutput, msg="Wrong number of lines in output")
    
    compline = 0
    self.assertEqual(outputLines[compline], "Start of ./scripts/kong_add_upstream", msg="Error in line " + str(compline+1))
    compline += 1
    if removeOtherTargets:
      self.assertEqual(outputLines[compline], "Will remove other targets", msg="Error in line " + str(compline+1))
    else:
      self.assertEqual(outputLines[compline], "Not removing other targets", msg="Error in line " + str(compline+1))
      
    compline += 1
    self.assertEqual(outputLines[compline], " Add (or update) upstream " + serviceName + " with target " + targetName + " " + self.kong_server, msg="Error in line " + str(compline+1))
    
    if not expectUpstreamToExist:
      compline += 1
      self.assertEqual(outputLines[compline], "Upstream dosen't already exist - Creating", msg="Error in line " + str(compline+1))

    compline += 1
    self.assertEqual(outputLines[compline], "Adding target to upstream", msg="Error in line " + str(compline+1))
    compline += 1
    #self.assertEqual(outputLines[5], "Target ID:dfe001ec-8ce2-438e-9793-71a694aaea35", msg="Error in line 6")
    if removeOtherTargets:
      compline += 1
      self.assertEqual(outputLines[compline], "Now removing all other targets", msg="Error in line " + str(compline+1))

    if removeOtherTargets:
      compline += 1
      gotNotRemoving = False
      while not (outputLines[compline].startswith("Number of targets removed: ")):
        if outputLines[compline] == "Not removing - current target":
          gotNotRemoving = True
        else:
          a = outputLines[compline].split(' ')
          self.assertEqual(len(a), 5, msg="Badly formed line")
          if a[2] in targetsExpectedToBeRemoved:
            if targetsExpectedToBeRemoved[a[2]]["found"]:
              self.assertFalse(True,msg="Removed same target twice")            
            targetsExpectedToBeRemoved[a[2]]["found"] = True
          else:
            self.assertFalse(True,msg="Removed target we didn't expect: " + outputLines[compline])
        compline += 1
      for x in targetsExpectedToBeRemoved:
        if not targetsExpectedToBeRemoved[x]["found"]:
          self.assertFalse(True, msg="Did not remove target " + targetsExpectedToBeRemoved[x]["name"])
      
      if not gotNotRemoving:
        self.assertTrue(False, msg="Did not recieve Not removing notice")
    
      #compline += 1 Previous step incremented compline already
      self.assertEqual(outputLines[compline], "Number of targets removed: " + str(len(targetsExpectedToBeRemoved)), msg="Error in line " + str(compline+1))


    compline += 1
    self.assertEqual(outputLines[compline], "End of ./scripts/kong_add_upstream", msg="Error in line " + str(compline+1))

    #compline is zero based
    self.assertEqual(compline+1,expectedLinesInOutput, msg="Wrong number of lines PROCESSED from output")


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
    self.add_new_upstream(test_service_name, test_target_name1, True, expectUpstreamToExist=False, targetsExpectedToBeRemoved=[])
    upstreamTargets = self.get_upstream_targetlist(test_service_name)
    self.assertEqual(len(upstreamTargets), 1, msg="Wrong number of targets")
    self.assertEqual(upstreamTargets[0]["target"],test_target_name1, msg="Target mismatch")
    
    #verify upstreamlist changed correctly
    upstreamList = self.get_upstream_targetlist(test_service_name)
    self.assertEqual(len(upstreamList),1)
    self.assertEqual(upstreamList[0]["target"],test_target_name1)

  def test_add_existing_new_upstream_to_same_target(self):
    test_service_name = "service_name"
    test_target_name1 = "target_Name:8022"
    self.delete_all_upstreams()
    self.add_new_upstream(test_service_name, test_target_name1, True, expectUpstreamToExist=False, targetsExpectedToBeRemoved=[])
    self.add_new_upstream(test_service_name, test_target_name1, True, expectUpstreamToExist=True, targetsExpectedToBeRemoved=[])
    upstreamTargets = self.get_upstream_targetlist(test_service_name)
    self.assertEqual(len(upstreamTargets), 1, msg="Wrong number of targets")
    self.assertEqual(upstreamTargets[0]["target"],test_target_name1, msg="Target mismatch")

    #verify upstreamlist changed correctly
    upstreamList = self.get_upstream_targetlist(test_service_name)
    self.assertEqual(len(upstreamList),1)
    self.assertEqual(upstreamList[0]["target"],test_target_name1)

  def test_add_existing_upstream_and_remove_other_targets(self):
    test_service_name = "service_name"
    test_target_name1 = "target_Name:8022"
    test_target_name2 = "target_Name2:8022"
    self.delete_all_upstreams()
    self.add_new_upstream(test_service_name, test_target_name1, True, expectUpstreamToExist=False, targetsExpectedToBeRemoved=[])
    self.add_new_upstream(test_service_name, test_target_name2, True, expectUpstreamToExist=True, 
      targetsExpectedToBeRemoved={test_target_name1: {"name": test_target_name1, "found": False}}
    )
    #verify upstreamlist changed correctly
    upstreamTargets = self.get_upstream_targetlist(test_service_name)
    self.assertEqual(len(upstreamTargets), 1, msg="Wrong number of targets")
    self.assertEqual(upstreamTargets[0]["target"],test_target_name2, msg="Target mismatch")

  def test_add_existing_upstream_and_donot_remove_other_targets(self):
    test_service_name = "service_name"
    test_targets = {}
    test_targets["target_Name1:8022"] = {"name": "target_Name1:8022", "found": False}
    test_targets["target_Name2:8022"] = {"name": "target_Name2:8022", "found": False}
    test_targets["target_Name3:8022"] = {"name": "target_Name3:8022", "found": False}
    test_targets["target_Name4:8022"] = {"name": "target_Name4:8022", "found": False}
    test_targets["target_Name5:8022"] = {"name": "target_Name5:8022", "found": False}
    self.delete_all_upstreams()
    num = 0
    for x in test_targets:
      num += 1
      self.add_new_upstream(test_service_name, test_targets[x]["name"], removeOtherTargets=False, expectUpstreamToExist=(num != 1), targetsExpectedToBeRemoved={})

    #verify upstreamlist changed correctly
    upstreamTargets = self.get_upstream_targetlist(test_service_name)
    self.assertEqual(len(upstreamTargets), 5, msg="Wrong number of targets")
    
    for y in upstreamTargets:
      print(y)
    
    for x in test_targets:
      for y in upstreamTargets:
        if y["target"]==test_targets[x]["name"]:
          if test_targets[x]["found"]:
            self.assertTrue(False,msg="Found same target twice - " + y["target"])
          test_targets[x]["found"]=True

    for x in test_targets:
      self.assertTrue(test_targets[x]["found"], msg="Target not found")

  def test_add_existing_upstream_and_remove_five_other_targets(self):
    test_service_name = "service_name"
    test_targets = {}
    test_targets["target_Name1:8022"] = {"name": "target_Name1:8022", "found": False}
    test_targets["target_Name2:8022"] = {"name": "target_Name2:8022", "found": False}
    test_targets["target_Name3:8022"] = {"name": "target_Name3:8022", "found": False}
    test_targets["target_Name4:8022"] = {"name": "target_Name4:8022", "found": False}
    test_targets["target_Name5:8022"] = {"name": "target_Name5:8022", "found": False}
    mainTestTarget = "main_target:8022"
    self.delete_all_upstreams()
    num = 0
    for x in test_targets:
      num += 1
      self.add_new_upstream(test_service_name, test_targets[x]["name"], removeOtherTargets=False, expectUpstreamToExist=(num != 1), targetsExpectedToBeRemoved={})

    upstreamTargets = self.get_upstream_targetlist(test_service_name)
    self.assertEqual(len(upstreamTargets), 5, msg="Wrong number of targets")

    #Now remove 5 targets
    self.add_new_upstream(
      test_service_name, mainTestTarget, 
      removeOtherTargets=True, 
      expectUpstreamToExist=(num != 1), 
      targetsExpectedToBeRemoved=copy.deepcopy(test_targets)
    )


    upstreamTargets = self.get_upstream_targetlist(test_service_name)
    self.assertEqual(len(upstreamTargets), 1, msg="Wrong number of targets")

    self.assertEqual(upstreamTargets[0]["target"],mainTestTarget, msg="Target mismatch")
