import enum


def adapt_enum(enum_obj):
    """
    SQLITE adapter for custom column type support.
    :param enum_obj:
    :return:
    """
    return "{};{}".format(enum_obj.name, enum_obj.value)


def convert_enum(enum_class):
    """
    SQLITE connector for custom column type support.
    :param enum_class:
    :return: converter function.
    """

    def func(s):
        e_type, val = s.decode("utf-8").split(";")
        if e_type in enum_class.__members__.keys():
            return enum_class[e_type]

        return None

    return func


def from_value(enumeration, value):
    """
    Helper function that restores Enum from it's value.
    :param enumeration:
    :param value:
    :return:
    """
    for en in enumeration:
        if en.value == value:
            return en


class Stages(enum.Enum):
    Incoming = "Incoming"
    Backlog = "Backlog"
    ToDo = "ToDo"
    Today = "Today"
    Doing = "Doing"
    Waiting = "Waiting"
    Done = "Done"


class Projects(enum.Enum):
    Money = "Money"
    Health = "Health"
    Business = "Business"
    Fun = "Fun"
    Relationships = "Friends & Family"
    Development = "Self-development"
    Environment = "Environment"


class Generators(enum.Enum):
    Daily = "Daily"
    Monthly = "Monthly"
