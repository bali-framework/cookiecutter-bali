ALWAYS_EXCLUDE = {"id", "is_active"}
EXCLUDE_FOR_API = {*ALWAYS_EXCLUDE, "{{cookiecutter.business_key}}", "created_time", "updated_time"}
BUSINESS_KEY_PATH = "/{{{cookiecutter.business_key}}}"
BUSINESS_KEY_PATH = "/{}".format("{{cookiecutter.business_key}}")
EMPTY_PATH = ""
