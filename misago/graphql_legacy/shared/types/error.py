from ariadne import ObjectType

error_type = ObjectType("Error")

error_type.set_alias("location", "loc")
error_type.set_alias("message", "msg")
