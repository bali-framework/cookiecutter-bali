ALWAYS_EXCLUDE = ["id", "is_active"]
EXCLUDE_AUTO_DATETIME = [*ALWAYS_EXCLUDE, "created_time", "updated_time"]
UUID_PATH = "/{uuid}"
EMPTY_PATH = ""
