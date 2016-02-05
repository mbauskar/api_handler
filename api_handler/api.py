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
	app_name = api_config.app_name

	if len(parts) <= 2:
		if parts[1] == 'login':
			frappe.local.form_dict.cmd = '.'.join(map(str,[app_name,parts[1]]))
			frappe.local.form_dict.op = "login"
			return handler.handle()

	elif len(parts) == 4 and parts[2] == "method":
		version = parts[1]
		if api_config and version not in api_config.allowed_versions:
			return report_error(417, "Invalid API Version, please check api configurations")

		method_name = parts[3]
		method = '.'.join(map(str,[app_name, "api.versions", version.replace(".", "_"), method_name]))

		frappe.local.form_dict.cmd = method
		return handler.handle()

	elif (len(parts) <= 4 or len(parts) >= 5) and parts[2] == "resource":
		version = parts[1] or ""
		
		frappe.local.form_dict.doctype = parts[3] or ""
		frappe.local.form_dict.name = parts[4] if len(parts) == 5 else ""

		if api_config and version not in api_config.allowed_versions:
			return report_error(417, "Invalid API Version, please check api configurations")

		method = '.'.join(map(str,[api_config.app_name, "api.versions", version.replace(".", "_"), "rest_api"]))
		frappe.local.form_dict.cmd = method

		if not is_valid_min_max_filters():
			return report_error(417, "Invalid Min or Max filter")

		return handler.handle()

	else:
		#invalid url
		return report_error(417,"Invalid URL")

def is_valid_version(version, api_config=None):
	if api_config and version in api_config.allowed_versions:
		return True
	else:
		return False	

def is_valid_min_max_filters():
	# validate min or max filters
	keys = map(lambda key: key.lower(), frappe.local.form_dict.keys())

	_filter = [key for key in keys if key in ["min", "max"]]

	if len(_filter) == 1 and "min" in keys and frappe.local.form_dict.min:
		key = "min"
		field = json.loads(frappe.local.form_dict.min)
	elif len(_filter) == 1 and "max" in keys and frappe.local.form_dict.max:
		key = "max"
		field = json.loads(frappe.local.form_dict.max)
	else:
		return True
	
	if isinstance(field, basestring):
		return build_min_max_filter(key, field)
	else:
		return False

def build_min_max_filter(_filter, field):
	if not _filter and not field:
		return False
	else:
		_field = "{_filter}({field}) as {field}".format(_filter=_filter, field=field)
		api_fields = json.loads(frappe.local.form_dict.fields or "[]")
		
		if api_fields and isinstance(api_fields, list):
			api_fields.append(_field)
		elif api_fields and isinstance(api_fields, basestring):
			api_fields = [api_fields, _field]
		else:
			api_fields = ["name", _field]
	
		# frappe.local.form_dict.fields = json.dumps(api_fields)
		frappe.local.form_dict.pop(_filter)
		frappe.local.form_dict["fields"] = '"{}"'.format(_field)

		return True
