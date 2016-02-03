# -*- coding: utf-8 -*-
# Copyright (c) 2015, New Indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import os
import frappe
from frappe.model.document import Document

class APIVersion(Document):
	# def autoname(self):
	# 	pass

	def validate(self):
		# create the directory structure
		# app_name/app_name/versions/version/ add __init__.py
		"""If in `developer_mode`, create folder for api version"""
		self.app_name = frappe.db.get_value("API Configuration", "API Configuration", "app_name")
		if not self.app_name:
			frappe.throw("Please first configure the APP Name to create the api version directory")
		elif frappe.conf.get("developer_mode"):
			self.create_api_version_folder()

	def create_api_version_folder(self):
		"""Creates a folder `[app]/versions/[version]` and adds `__init__.py`"""
		module_path = frappe.get_app_path(self.app_name, "versions",self.name)
		if not os.path.exists(module_path):
			os.mkdir(module_path)
			with open(os.path.join(module_path, "__init__.py"), "w") as f:
				f.write("")