# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals

# BEWARE don't put anything in this file except exceptions

from werkzeug.exceptions import NotFound
from MySQLdb import ProgrammingError as SQLError

class ValidationError(Exception):
	status_code = 417

class AuthenticationError(Exception):
	status_code = 401

class PermissionError(Exception):
	def __init__(self,operation,message):
		self.operation = operation
		self.message = message
	status_code = 403

class DoesNotExistError(ValidationError):
	status_code = 404

class NameError(Exception):
	status_code = 409

class OutgoingEmailError(Exception):
	status_code = 501

class SessionStopped(Exception):
	status_code = 503

class UnsupportedMediaType(Exception):
	status_code = 415

class Redirect(Exception):
	status_code = 301

class NoAllowed(Exception):
	status_code = 403

class NotImplementedException(Exception):
	status_code = 501
	message = "Not Yet Implemented"

class DuplicateEntryError(NameError):pass
class InvalidDataError(ValidationError): pass
class UnknownDomainError(Exception): pass
class MappingMismatchError(ValidationError): pass
class MandatoryError(ValidationError): pass
class InvalidSignatureError(ValidationError): pass
class CannotChangeConstantError(ValidationError): pass
class TimestampMismatchError(ValidationError): pass
class EmptyTableError(ValidationError): pass
class InvalidEmailAddressError(ValidationError): pass
class TemplateNotFoundError(ValidationError): pass
class UniqueValidationError(ValidationError): pass
class UserRegisteredButDisabledError(ValidationError):pass
class UserAlreadyRegisteredError(ValidationError):pass
class UserRegisterationError(ValidationError):pass
class ForgotPasswordOperationFailed(ValidationError):pass
class InvalidPasswordError(ValidationError):pass
class GetUserProfileOperationFailed(ValidationError):pass
class UserProfileUpdationFailed(ValidationError):pass
class LogOutOperationFailed(ValidationError):pass
class GetStateInfoOperationFailed(ValidationError):pass
class ImageUploadError(ValidationError):pass
class SearchGroupOperationFailed(ValidationError):pass
class GetPropertyOperationFailed(ValidationError):pass
class ElasticSearchException(ValidationError):pass
class ElasticInvalidInputFormatError(ValidationError):pass
class OperationFailed(ValidationError):pass