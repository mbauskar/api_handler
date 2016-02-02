# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt
from __future__ import unicode_literals

import json
import frappe
from frappe import _
import handler
from response import build_response,report_error

def handle(api_config):
	"""
	Handler for `/api_name` methods
	**api_name = configured in api_hander hooks 
	### Examples:

	`/api_name/version/{methodname}` will call a whitelisted method
	
	"""
	parts = frappe.request.path[1:].split("/",5)
	method_name = version = api_name = method = None
	# return report_error(1, len(parts) >= 5 and parts[2] == "resource")
	if len(parts) <= 2:
		if parts[1] == 'login':
			frappe.local.form_dict.cmd = '.'.join(map(str,[parts[0],parts[1]]))
			frappe.local.form_dict.op = "login"
			return handler.handle()

	elif len(parts) == 4 and parts[2] == "method":
		version = parts[1]
		if not is_valid_version(version): 
			return report_error(417, "Invalid API Version")

		method_name = parts[3]
		method = '.'.join(map(str,[api_config.app_name, "versions", version, method_name]))

		frappe.local.form_dict.cmd = method
		return handler.handle()

	elif (len(parts) <= 4 or len(parts) >= 5) and parts[2] == "resource":
		version = parts[1]
		if not is_valid_version(version): 
			return report_error(417, "Invalid API Version")

		method = '.'.join(map(str,[api_config.app_name, "versions", version, "rest_api"]))
		frappe.local.form_dict.cmd = method
		return report_error(417, frappe.local.form_dict.cmd)
		return handler.handle()

	else:
		#invalid url
		return report_error(417,"Invalid URL")

def is_valid_version(version, api_config=None):
	if api_config:
		allowed_versions = allowed_versions.allowed_versions
	else:
		versons = frappe.db.get_values("Allowed API Version", {"parent": "API Configuration"}, "api_version")
		allowed_versions = [v[0] for v in versons]

	if version not in allowed_versions:
		return False
	else:
		return True