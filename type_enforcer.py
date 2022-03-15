import inspect
from inspect import signature, currentframe
import functools

# pycheckarg --------------------------------------------- :
class ArgumentChecker:
    """
    currenty supports checking for only built-ins
    """

    @staticmethod
    def check_1(f_ref, f_args) -> None:
        for p in signature(f_ref).parameters.values():
            if not isinstance(f_args[p.name], p.annotation):
                raise TypeError(
                    f"InvalidArgumentType {type(f_args[p.name])} for argument '{p}'"
                )

    @staticmethod
    def check_2() -> None:
        # caller_function_name = currentframe().f_back.f_code.co_name
        previous_frame = currentframe().f_back
        *_, caller_function_name, _, _ = inspect.getframeinfo(previous_frame)
        f_ref, f_args = eval(caller_function_name), previous_frame.f_locals
        ArgumentChecker.check_1(f_ref, f_args)

    @staticmethod
    def arg_check_decorator(f_ref) -> None:
        @functools.wraps(
            f_ref
        )  # NOTE: as you remove this , you'll notice the real use of this .
        def wrapper(*args, **kwargs):
            arg_dict = dict(zip(f_ref.__code__.co_varnames, args))
            for p_name, p_annotation in f_ref.__annotations__.items():
                if not isinstance(arg_dict[p_name], p_annotation):
                    raise TypeError(
                        f"InvalidArgumentType {type(arg_dict[p_name])} for argument '{p_name}:{p_annotation}'"
                    )
            return f_ref(*args, *kwargs)

        return wrapper


# tests --------------------------------------------- :
import unittest

pycheckarg = ArgumentChecker


class BasicPyArgCheckTests(unittest.TestCase):
    def test_checking_types_1_Negetive(self):
        """check : error raised if invalid type argument is passed"""

        @pycheckarg.arg_check_decorator
        def dummytestfunction(arg1: int):
            pass

        with self.assertRaises(TypeError):
            wrong_argument = dict(key=1)
            dummytestfunction(wrong_argument)

    def test_checking_types_2_Posetive(self):
        """check : no error raised if argument of matching type is passed"""

        @pycheckarg.arg_check_decorator
        def dummytestfunction(arg1: int, arg2):
            pass

        right_argument_1 = 43
        argument_2 = (
            1,
            2,
        )
        dummytestfunction(right_argument_1, argument_2)

        self.assertTrue(True)

    def test_checking_types_3_Posetive(self):
        """check : no error raised if correct type of arguments passed"""

        @pycheckarg.arg_check_decorator
        def dummytestfunction(
            arg1: int, arg2: dict, arg3: tuple, arg4: str, arg5: list, arg6: object
        ):
            pass

        class DummyTestClass:
            pass

        right_test_arg1 = 22
        right_test_arg2 = dict()
        right_test_arg3 = (
            1,
            2,
        )
        right_test_arg4 = "xyz"
        right_test_arg5 = [1, 2, 3, 4]
        right_test_arg6 = DummyTestClass()

        dummytestfunction(
            right_test_arg1,
            right_test_arg2,
            right_test_arg3,
            right_test_arg4,
            right_test_arg5,
            right_test_arg6,
        )

        self.assertTrue(True)


class TestBuiltinsTypeCheck(unittest.TestCase):
    def setUp(self):
        @pycheckarg.arg_check_decorator
        def int_check(_arg: int):
            return None

        self.int_check = int_check

        @pycheckarg.arg_check_decorator
        def tuple_check(_arg: tuple):
            return None

        self.tuple_check = tuple_check

        @pycheckarg.arg_check_decorator
        def list_check(_arg: list):
            return None

        self.list_check = list_check

        @pycheckarg.arg_check_decorator
        def dict_check(_arg: dict):
            return None

        self.dict_check = dict_check

        class DummyTestClass: pass
        self.DummyTestClass = DummyTestClass
        @pycheckarg.arg_check_decorator
        def object_check(_arg: DummyTestClass):
            return None

        self.object_check = object_check

    def test_checking_int(self):

        with self.assertRaises(TypeError):
            non_integer_value = dict()
            self.int_check(non_integer_value)

    def test_checking_tuple(self):

        with self.assertRaises(TypeError):
            non_tuple_value = dict()
            self.tuple_check(non_tuple_value)
    def test_checking_list(self):

        with self.assertRaises(TypeError):
            non_list_value = dict()
            self.list_check(non_list_value)
    def test_checking_dict(self):

        with self.assertRaises(TypeError):
            non_dict_value = 33
            self.dict_check(non_dict_value)
    def test_checking_object(self):

        with self.assertRaises(TypeError):
            non_object_value = "234"
            self.object_check(non_object_value)

# main --------------------------------------------- :
if __name__ == "__main__":
    # TODO: write test cases
    unittest.main()
