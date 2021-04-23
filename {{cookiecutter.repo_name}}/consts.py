ALWAYS_EXCLUDE = ["id", "is_active"]
EXCLUDE_FOR_API = [*ALWAYS_EXCLUDE, "uuid", "created_time", "updated_time"]
UUID_PATH = "/{uuid}"
EMPTY_PATH = ""
