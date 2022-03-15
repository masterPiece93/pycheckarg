import inspect
from inspect import signature, currentframe
import functools
class ArgumentChecker:
    '''
    currenty supports checking for only built-ins
    '''
    @staticmethod
    def check_1(f_ref, f_args)->None:
        for p in signature(f_ref).parameters.values():
            if not isinstance(f_args[p.name],p.annotation):
                raise TypeError(f"InvalidArgumentType {type(f_args[p.name])} for argument '{p}'")
    @staticmethod
    def check_2()->None:
        # caller_function_name = currentframe().f_back.f_code.co_name
        previous_frame = currentframe().f_back
        *_, caller_function_name, _,_ = inspect.getframeinfo(previous_frame)
        f_ref, f_args = eval(caller_function_name), previous_frame.f_locals
        ArgumentChecker.check_1(f_ref, f_args)
    
    def arg_check_decorator(f_ref)->None:
        @functools.wraps(f_ref) # NOTE: as you remove this , you'll notice the real use of this .
        def wrapper(*args, **kwargs):
            arg_dict = dict(zip(f_ref.__code__.co_varnames, args))
            for p_name, p_annotation in f_ref.__annotations__.items():
                if not isinstance(arg_dict[p_name],p_annotation):
                    raise TypeError(f"InvalidArgumentType {type(arg_dict[p_name])} for argument '{p_name}:{p_annotation}'")
            return f_ref(*args, *kwargs)
        return wrapper
 
if __name__ == '__main__':
    @ArgumentChecker.arg_check_decorator
    def f(a:int,b:dict,c:int=0): print("PASSED")
