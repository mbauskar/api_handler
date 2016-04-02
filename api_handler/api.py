# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt
from __future__ import unicode_literals

import json
import frappe
from frappe import _
import handler
from response import build_response,report_error

def handle():
	"""
	Handler for `/api_name` methods
	**api_name = configured in api_hander hooks 
	### Examples:

	`/api_name/version/{methodname}` will call a whitelisted method
	
	"""
	parts = frappe.request.path[1:].split("/",4)
	method_name = version = api_name = method = None

	if len(parts) <= 2:
		if parts[1] == 'login':
			frappe.local.form_dict.cmd = '.'.join(map(str,[parts[0],"login"]))
			frappe.local.form_dict.op = "login"
			return handler.handle()

	else:
		api_name = parts[0]
		version = parts[2].replace(".", "_")
		if parts[3] == "method":
			method_name = parts[4]
			method = '.'.join(map(str,[api_name,"api.versions",version,method_name]))
			frappe.local.form_dict.cmd = method
			return handler.handle()
		elif parts[3] == "resource":
			resource = parts[4].split("/")[0]
			method = '.'.join(map(str,[api_name,"api.versions",version,resource, "get"]))
			frappe.local.form_dict.cmd = method
			frappe.local.form_dict.resource = parts[4].split("/")[1:]
			return handler.handle()
		else:
			return report_error(417,"Invalid URL")
