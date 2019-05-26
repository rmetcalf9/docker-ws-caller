from TestHelperSuperClass import testHelperSuperClass

class local_helpers(testHelperSuperClass):
  pass

class test_kong_add_jwt_and_acl_plugins(local_helpers):
  def test_noArgs(self):
    cmdToExecute = "./scripts/kong_add_jwt_and_acl_plugins"
    expectedOutput = ""
    expectedOutput += "Start of ./scripts/kong_add_jwt_and_acl_plugins\n"
    expectedOutput += "Wrong number of arguments expected 6 - got 0\n"
    expectedOutput += "Recieved args:\n"
    expectedOutput += "['./scripts/kong_add_jwt_and_acl_plugins']\n"
    expectedOutput += "-\n"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1, False)

  def test_addWithWhitelist(self):

    serviceName = "TestServiceName"
    route = {
      "protocol": "http",
      "host": "route.host.com",
      "path": "/ppp"
    }

    self.deleteService(serviceName)
    serviceResp = self.createServiceAndRoute(serviceName, route)

    cmdToExecute = "./scripts/kong_add_jwt_and_acl_plugins"
    cmdToExecute += " " + self.kong_server
    cmdToExecute += " " + serviceName
    cmdToExecute += " " + "\"some_cookie\""
    cmdToExecute += " " + "\"aclWhite1 aclWhite2\""
    cmdToExecute += " " + "\"\""
    cmdToExecute += " " + "kong_iss"
    expectedOutput = ""
    expectedOutput += "Start of ./scripts/kong_add_jwt_and_acl_plugins\n"
    expectedOutput += "Recieved Args:\n"
    expectedOutput += "              kongURL:http://127.0.0.1:8381:\n"
    expectedOutput += "         SERVICE_NAME:TestServiceName:\n"
    expectedOutput += "      JWT_COOKIE_NAME:some_cookie:\n"
    expectedOutput += " AUTHED_ACL_WHITELIST:aclWhite1 aclWhite2:\n"
    expectedOutput += " AUTHED_ACL_BLACKLIST::\n"
    expectedOutput += "       key_claim_name:kong_iss:\n"
    expectedOutput += " AUTHED_ACL_WHITELIST_l: ['aclWhite1', 'aclWhite2']\n"
    expectedOutput += " AUTHED_ACL_BLACKLIST_l: []\n"
    expectedOutput += "Getting a list of plugins\n"
    expectedOutput += "Adding JWT plugin\n"
    expectedOutput += "Adding ACL plugin\n"
    expectedOutput += "End of ./scripts/kong_add_jwt_and_acl_plugins\n"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, False)

    #Query plugins
    resp, respCode = self.callKongService("/services/" + serviceName + "/plugins", {}, "get", None, [200])
    jwtPlugin = None
    aclPlugin = None
    for x in resp["data"]:
      if x["name"] == "jwt":
        if jwtPlugin is not None:
          self.assertTrue(False,msg="ERROR Two jwt plugins")
        jwtPlugin = x
      if x["name"] == "acl":
        if aclPlugin is not None:
          self.assertTrue(False,msg="ERROR Two acl plugins")
        aclPlugin = x
    if jwtPlugin is None:
      self.assertTrue(False,msg="ERROR Missing jwtPlugin")
    if aclPlugin is None:
      self.assertTrue(False,msg="ERROR Missing aclPlugin")

    #ensure it's a whitelist not a blacklist
    self.assertEqual(aclPlugin["config"]["whitelist"],["aclWhite1", "aclWhite2"])

  def test_addWithBlacklist(self):

    serviceName = "TestServiceName"
    route = {
      "protocol": "http",
      "host": "route.host.com",
      "path": "/ppp"
    }

    self.deleteService(serviceName)
    serviceResp = self.createServiceAndRoute(serviceName, route)

    cmdToExecute = "./scripts/kong_add_jwt_and_acl_plugins"
    cmdToExecute += " " + self.kong_server
    cmdToExecute += " " + serviceName
    cmdToExecute += " " + "\"some_cookie\""
    cmdToExecute += " " + "\"\""
    cmdToExecute += " " + "\"aclBlack1 aclBlack2\""
    cmdToExecute += " " + "kong_iss"
    expectedOutput = ""
    expectedOutput += "Start of ./scripts/kong_add_jwt_and_acl_plugins\n"
    expectedOutput += "Recieved Args:\n"
    expectedOutput += "              kongURL:http://127.0.0.1:8381:\n"
    expectedOutput += "         SERVICE_NAME:TestServiceName:\n"
    expectedOutput += "      JWT_COOKIE_NAME:some_cookie:\n"
    expectedOutput += " AUTHED_ACL_WHITELIST::\n"
    expectedOutput += " AUTHED_ACL_BLACKLIST:aclBlack1 aclBlack2:\n"
    expectedOutput += "       key_claim_name:kong_iss:\n"
    expectedOutput += " AUTHED_ACL_WHITELIST_l: []\n"
    expectedOutput += " AUTHED_ACL_BLACKLIST_l: ['aclBlack1', 'aclBlack2']\n"
    expectedOutput += "Getting a list of plugins\n"
    expectedOutput += "Adding JWT plugin\n"
    expectedOutput += "Adding ACL plugin\n"
    expectedOutput += "End of ./scripts/kong_add_jwt_and_acl_plugins\n"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, False)

    #Query plugins
    resp, respCode = self.callKongService("/services/" + serviceName + "/plugins", {}, "get", None, [200])
    jwtPlugin = None
    aclPlugin = None
    for x in resp["data"]:
      if x["name"] == "jwt":
        if jwtPlugin is not None:
          self.assertTrue(False,msg="ERROR Two jwt plugins")
        jwtPlugin = x
      if x["name"] == "acl":
        if aclPlugin is not None:
          self.assertTrue(False,msg="ERROR Two acl plugins")
        aclPlugin = x
    if jwtPlugin is None:
      self.assertTrue(False,msg="ERROR Missing jwtPlugin")
    if aclPlugin is None:
      self.assertTrue(False,msg="ERROR Missing aclPlugin")

    #ensure it's a whitelist not a blacklist
    self.assertEqual(aclPlugin["config"]["blacklist"],["aclBlack1", "aclBlack2"])
