import functools
import sentry_sdk
from os import getenv


def sentry(func):
    """ Wraps function with Sentry so that error reporting will work in pytest as well as in production """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        environment = getenv("ENVIRONMENT", default="development")
        sentry_sdk.init(
            "https://a20cc578312643c7ac874588037f098c@o361657.ingest.sentry.io/5413698",
            traces_sample_rate=1.0,
            environment=environment,
        )
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Alternatively the argument can be omitted
            sentry_sdk.capture_exception(e)
            raise e

    return wrapper


def tag_dtype(
    _func=None, *, class_name_partial: str = None, open_tag="[b]", close_tag="[/b]"
):
    """
    Parses text returned by a function and replaces it with span tags that use the data_type from the function's
    argument as part of the tag's class name..

    Args:
        class_name_partial (str, optional): Text fragment to build class name in span tag. Default to using
            value stored on data_type of the wrapped function.
        open_tag (str, optional): opening tag that will be replaced with opening span tag.
        close_tag (str, optional) closing tag that will be replaced with closing span tag.

    Returns:
        str: Original text is updated to include span tags.

    """

    def wrapper_outer(func):
        @functools.wraps(func)
        def wrapper_inner(args, data_type, **kwargs):
            result = func(args, data_type=data_type, **kwargs)
            _class_name_partial = class_name_partial or data_type
            class_name_outer = f"highlight-outer__{_class_name_partial}"
            class_name_inner = f"highlight-inner__{_class_name_partial}"
            result = result.replace(
                open_tag,
                f'<span class="{class_name_outer}"><span class="{class_name_inner}">',
            )
            result = result.replace(close_tag, "</span></span>")
            return result

        return wrapper_inner

    if _func is None:
        return wrapper_outer
    else:
        return wrapper_outer(_func)


def tag(
    _func=None, *, class_name_partial: str = None, open_tag="[b]", close_tag="[/b]"
):
    """
    Parses text returned by a function and replaces it with span tags that use a custom classname.

    Args:
        class_name_partial (str, optional): Text fragment to build class name in span tag. Default to using
            value stored on data_type of the wrapped function.
        open_tag (str, optional): opening tag that will be replaced with opening span tag.
        close_tag (str, optional) closing tag that will be replaced with closing span tag.

    Returns:
        str: Original text is updated to include span tags.

    """

    def wrapper_outer(func):
        @functools.wraps(func)
        def wrapper_inner(args, **kwargs):
            result = func(args, **kwargs)
            _class_name_partial = class_name_partial
            class_name_outer = f"highlight-outer__{_class_name_partial}"
            class_name_inner = f"highlight-inner__{_class_name_partial}"
            result = result.replace(
                open_tag,
                f'<span class="{class_name_outer}"><span class="{class_name_inner}">',
            )
            result = result.replace(close_tag, "</span></span>")
            return result

        return wrapper_inner

    if _func is None:
        return wrapper_outer
    else:
        return wrapper_outer(_func)
