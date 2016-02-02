# -*- coding: utf-8 -*-
# Copyright (c) 2015, New Indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

import json

class APIConfiguration(Document):
	def validate(self):
		# check if app name is valid or not
		if self.app_name not in frappe.get_installed_apps():
			frappe.throw("{0} app name is either invalid or not install in the system<br>\
				app name should be <b>{1}<b>".format(self.app_name, " or ".join(frappe.get_installed_apps())))

		# app name is valid create api_config and write api_config.json
		api_config = {
			"app_name": self.app_name,
			"api_name": self.api_name,
			"allowed_versions": map(lambda row: row.api_version, self.versions)
		}

		file_name = "{}/api_config.json".format(frappe.utils.get_site_path())
		with open(file_name, "w") as f:
			f.write(json.dumps(api_config, sort_keys=True, indent=4))
