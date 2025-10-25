from . import __version__ as app_version

app_name = "ivendnext_ai_chat"
app_title = "iVendNext AI Chat"
app_publisher = "iVendNext"
app_description = "Production-ready AI Chatbot for Frappe Framework"
app_email = "info@ivendnext.com"
app_license = "MIT"

# Includes in <head>
# ------------------

app_include_css = "/assets/ivendnext_ai_chat/css/ivendnext_ai_chat.css"
app_include_js = [
    "/assets/ivendnext_ai_chat/js/ai_chat.bundle.js"
]

# include js, css files in header of desk.html
# app_include_css = "/assets/ivendnext_ai_chat/css/ivendnext_ai_chat.css"
# app_include_js = "/assets/ivendnext_ai_chat/js/ivendnext_ai_chat.js"

# include js, css files in header of web template
# web_include_css = "/assets/ivendnext_ai_chat/css/ivendnext_ai_chat.css"
# web_include_js = "/assets/ivendnext_ai_chat/js/ivendnext_ai_chat.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ivendnext_ai_chat/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "ivendnext_ai_chat.utils.jinja_methods",
# 	"filters": "ivendnext_ai_chat.utils.jinja_filters"
# }

# Installation
# ------------

after_install = "ivendnext_ai_chat.install.after_install"

# Uninstallation
# ------------

before_uninstall = "ivendnext_ai_chat.install.before_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ivendnext_ai_chat.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ivendnext_ai_chat.tasks.all"
# 	],
# 	"daily": [
# 		"ivendnext_ai_chat.tasks.daily"
# 	],
# 	"hourly": [
# 		"ivendnext_ai_chat.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ivendnext_ai_chat.tasks.weekly"
# 	],
# 	"monthly": [
# 		"ivendnext_ai_chat.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "ivendnext_ai_chat.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ivendnext_ai_chat.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ivendnext_ai_chat.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ivendnext_ai_chat.utils.before_request"]
# after_request = ["ivendnext_ai_chat.utils.after_request"]

# Job Events
# ----------
# before_job = ["ivendnext_ai_chat.utils.before_job"]
# after_job = ["ivendnext_ai_chat.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ivendnext_ai_chat.auth.validate"
# ]
