from TestHelperSuperClass import testHelperSuperClass
from executor import executeCommand
import python_Testing_Utilities

import docker
import copy
import time
client = docker.DockerClient(base_url='unix://var/run/docker.sock')

scriptName="docker_service_remove_non_live"

ws_name = "testing_ws"
image_prefix = "dockercloud/"

class local_helpers(testHelperSuperClass):
  def ensure_list_of_running_service_verisons(self, lis):
    required_service_names = []
    for x in lis:
      required_service_names.append(ws_name + "_" + x.replace('.','_'))

    services_to_stop = []
    services_to_start = copy.deepcopy(lis)
    for service in client.services.list():
      if service.name.startswith(ws_name):
        if service.name not in required_service_names:
          services_to_stop.append(service)
        else:
          required_service_names.remove(service.name)

    for service in services_to_stop:
      service.remove()
    for service_name in required_service_names:
      client.services.create(
        image="dockercloud/hello-world",
        name=service_name
      )
    time.sleep(0.5)

    baseImage = client.images.get("dockercloud/hello-world:latest")

    #Now create and delete images
    imgs_to_del = []
    imgs_to_create = copy.deepcopy(lis)
    for image in client.images.list():
      for tag in image.tags:
        if tag.startswith(image_prefix + ws_name + ":"):
          ver = tag[(len(image_prefix + ws_name) + 1):]
          if ver in imgs_to_create:
            #Image already in list we don't need to create it
            imgs_to_create.remove(ver)
          else:
            imgs_to_del.append(ver)

    for ver in imgs_to_create:
      baseImage.tag(image_prefix + ws_name + ":" + ver)
    for ver in imgs_to_del:
      client.images.remove(image_prefix + ws_name + ":" + ver)

  def assertVersionRunningList(self, lis, scriptoutput):
    required_service_names = []
    for x in lis:
      required_service_names.append(ws_name + "_" + x.replace('.','_'))

    running_service_names = []
    for service in client.services.list():
      if service.name.startswith(ws_name):
        running_service_names.append(service.name)

    if not python_Testing_Utilities.objectsEqual(required_service_names,running_service_names):
      self.printExecuteCommandOutput(scriptoutput)
      print("Expected services running:" + str(required_service_names))
      print("Actual services running:" + str(running_service_names))
      self.assertTrue(False,msg="Wrong services running")

    #Finally make sure images have been deleted
    # no need to check for created images as if they are not there
    # the service would not run
    for image in client.images.list():
      for tag in image.tags:
        if tag.startswith(image_prefix + ws_name + ":"):
          ver = tag[(len(image_prefix + ws_name) + 1):]
          if ver not in lis:
            self.printExecuteCommandOutput(scriptoutput)
            self.assertTrue(False,msg="Image " + tag + " was not removed")

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
    self.ensure_list_of_running_service_verisons([])

    version = "0.4.5"
    expectedOutput = "Start of ./scripts/" + scriptName + "\n"
    expectedOutput += "Given a service name and version stops all services and removes all images that don't match that version\n"
    expectedOutput += "ws_name:" + ws_name + "\n"
    expectedOutput += "version:" + version + "\n"
    expectedOutput += "image_prefix:" + image_prefix + "\n"
    expectedOutput += "Error - could not find live service\n"
    expectedOutput += "        (" + ws_name + "_" + version.replace('.','_') + ")\n"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/" + scriptName + " " + ws_name + " " + version + " " + image_prefix

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1, False)

    self.assertVersionRunningList([], a)


  def test_servicerunningnothingtostoporremove_differentversionrunning(self):
    version = "0.4.9"

    self.ensure_list_of_running_service_verisons(["0.4.5"])
    expectedOutput = "Start of ./scripts/" + scriptName + "\n"
    expectedOutput += "Given a service name and version stops all services and removes all images that don't match that version\n"
    expectedOutput += "ws_name:" + ws_name + "\n"
    expectedOutput += "version:" + version + "\n"
    expectedOutput += "image_prefix:" + image_prefix + "\n"
    expectedOutput += "Error - could not find live service\n"
    expectedOutput += "        (" + ws_name + "_" + version.replace('.','_') + ")\n"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/" + scriptName + " " + ws_name + " " + version + " " + image_prefix

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1, False)

    self.assertVersionRunningList(["0.4.5"], a)


  def test_servicerunningnothingtostoporremove(self):
    version = "0.4.5"

    self.ensure_list_of_running_service_verisons(["0.4.5"])
    expectedOutput = "Start of ./scripts/" + scriptName + "\n"
    expectedOutput += "Given a service name and version stops all services and removes all images that don't match that version\n"
    expectedOutput += "ws_name:" + ws_name + "\n"
    expectedOutput += "version:" + version + "\n"
    expectedOutput += "image_prefix:" + image_prefix + "\n"
    expectedOutput += "Check live service is running PASSED (testing_ws_0_4_5)\n"
    expectedOutput += "End of ./scripts/" + scriptName + "\n"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/" + scriptName + " " + ws_name + " " + version + " " + image_prefix

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, False)

    self.assertVersionRunningList(["0.4.5"], a)

  def test_servicerunningoneservicetoremove(self):
    version = "0.4.5"

    self.ensure_list_of_running_service_verisons(["0.4.5","0.4.0"])
    expectedOutput = "Start of ./scripts/" + scriptName + "\n"
    expectedOutput += "Given a service name and version stops all services and removes all images that don't match that version\n"
    expectedOutput += "ws_name:" + ws_name + "\n"
    expectedOutput += "version:" + version + "\n"
    expectedOutput += "image_prefix:" + image_prefix + "\n"
    expectedOutput += "Check live service is running PASSED (testing_ws_0_4_5)\n"
    expectedOutput += "Removing old service " + ws_name + "_0_4_0" + "\n"
    expectedOutput += "Removing Image " + image_prefix + ws_name + ":0.4.0" + "\n"
    expectedOutput += "End of ./scripts/" + scriptName + "\n"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/" + scriptName + " " + ws_name + " " + version + " " + image_prefix

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, False)

    self.assertVersionRunningList(["0.4.5"], a)

  def test_servicerunningtwoservicestoremove(self):
    version = "0.4.5"

    self.ensure_list_of_running_service_verisons(["0.4.5","0.4.0","0.3.4"])
    expectedOutput = "Start of ./scripts/" + scriptName + "\n"
    expectedOutput += "Given a service name and version stops all services and removes all images that don't match that version\n"
    expectedOutput += "ws_name:" + ws_name + "\n"
    expectedOutput += "version:" + version + "\n"
    expectedOutput += "image_prefix:" + image_prefix + "\n"
    expectedOutput += "Check live service is running PASSED (testing_ws_0_4_5)\n"
    expectedOutput += "Removing old service " + ws_name + "_0_3_4" + "\n"
    expectedOutput += "Removing old service " + ws_name + "_0_4_0" + "\n"
    expectedOutput += "Removing Image " + image_prefix + ws_name + ":0.3.4" + "\n"
    expectedOutput += "Removing Image " + image_prefix + ws_name + ":0.4.0" + "\n"
    expectedOutput += "End of ./scripts/" + scriptName + "\n"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/" + scriptName + " " + ws_name + " " + version + " " + image_prefix

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, False)

    self.assertVersionRunningList(["0.4.5"], a)
