# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import frappe.sessions
from response import build_response,report_error
import api_handler
import json	


def handle():
	"""handle request"""
	cmd = frappe.local.form_dict.cmd
	op = frappe.local.form_dict.op

	try :
		method = get_attr(cmd)

	except AttributeError, e:
		return report_error(500,"Invalid API-URL")

	if op == 'login':
		login_user()
	elif cmd != 'login':
		user = manage_user()

		if user:
			execute_cmd(cmd)

	return build_response("json")

def execute_cmd(cmd, async=False):
	"""execute a request as python module"""
 				
	method = get_attr(cmd)
	
	try:
		#check if whitelisted
		if frappe.session['user'] == 'Guest':
			if (method not in frappe.guest_methods):
				return report_error(403,"Not Allowed")		

		else:
			if not method in frappe.whitelisted:
				return report_error(403,"Not Allowed")
		
		ret = frappe.call(method, **frappe.form_dict)

		if isinstance(ret,dict):
			for key in ret:
				frappe.response[key] = ret[key]
		else:		
			frappe.response["data"] = ret
		frappe.response["code"] = 200		

	except Exception, e:
		http_status_code = getattr(e, "status_code", 500)
		message = getattr(e, "message", 500)
		report_error(http_status_code,message)

	else:
		pass

	finally:
		import time
		ts = int(time.time())
		frappe.response["timestamp"] = ts

def get_attr(cmd):
	"""get method object from cmd"""

	if '.' in cmd:
		method = frappe.get_attr(cmd)
	else:
		method = globals()[cmd]
	frappe.log("method:" + cmd)
	return method

def login_user():
	try: 
		cmd = frappe.local.form_dict.cmd
		method = get_attr(cmd)
		ret = frappe.call(method, **frappe.form_dict)
		return ret

	except Exception, e:
		http_status_code = getattr(e, "status_code", 500)
		message = getattr(e, "message", 500)
		report_error(http_status_code,message)
	
	finally:
		import time
		ts = int(time.time())
		frappe.response["timestamp"] = ts

def manage_user():
	if frappe.local.request.method in ["POST", "PUT", "DELETE"] and frappe.form_dict.data:
		data = json.loads(frappe.form_dict.data)		
		sid = data.get('sid')
		user_id = data.get('user_id')

		if not sid:
			report_error(417,"sid not provided")
			return False		

		elif sid and not user_id:
			report_error(417,"user_id not provided")
			return False

		elif sid and user_id:
			#user = frappe.db.get_value("User",{"user_id":user_id},"name")
			user = "aaa"
			if not user:
				report_error(417,"user_id not provided")
				return False
			else:
				try:
					frappe.form_dict["sid"] = sid 
					loginmgr = frappe.auth.LoginManager()
				except frappe.SessionStopped,e:
					http_status_code = getattr(e, "http_status_code", 500)
					frappe.response["code"] = http_status_code
					return False
		return True
	elif frappe.local.request.method=="GET":
		return True
	else:
		report_error(417,"Input not provided")
		return False			
