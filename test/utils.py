def unwrap_response(response, field=None):
    assert response.status_code == 200
    assert response.is_json
    json = response.get_json()
    assert json["success"]

    if field is not None:
        return json[field]
    return json


def api_call(client, method, *args, **kwargs):
    field = kwargs.pop("field")
    fn = getattr(client, method)
    response = fn(*args, **kwargs)
    return unwrap_response(response, field)


def api_get(client, *args, **kwargs):
    return api_call(client, "get", *args, **kwargs)


def api_post(client, *args, **kwargs):
    return api_call(client, "post", *args, **kwargs)


class SqlDumpContext:
    def __init__(self, obj, enable=True):
        self.application = obj
        if hasattr(self.application, "application"):
            self.application = self.application.application
        self.enable = True
        self.restore = self.application.config.get("SQLALCHEMY_ECHO", False)

    def __enter__(self):
        self.application.config["SQLALCHEMY_ECHO"] = self.enable

    def __exit__(self, exc_type, exc_value, traceback):
        self.application.config["SQLALCHEMY_ECHO"] = self.restore


def sql_dump(obj, enable=True):
    return SqlDumpContext(obj, enable)
