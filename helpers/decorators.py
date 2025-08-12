import functools
import time

from helpers.logger import logger


def retry_on_exceptions(*, exceptions, delay, max_retries, max_retry_exception=Exception, before_retry=None):
    def decorator(fn):
        def wrapper(self, *args, **kwargs):
            retries = 0

            while retries <= max_retries:
                try:
                    return fn(self, *args, **kwargs)
                except tuple(exceptions) as error:
                    retries += 1
                    logger.error(
                        f"Error caught: {error}. Attempt {retries}/{max_retries + 1}... Retrying after {delay} seconds.")

                    if retries <= max_retries:
                        if before_retry and hasattr(self, before_retry):
                            logger.info("Executing beforeRetry callback...")
                            getattr(self, before_retry)()

                        time.sleep(delay)  # Delay in seconds
                    else:
                        raise max_retry_exception(f"Failed after {max_retries} retries")

        return wrapper

    return decorator


def execute_method_when_finished(method_name):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            try:
                return fn(self, *args, **kwargs)
            finally:
                method = getattr(self, method_name)
                if method and callable(method):
                    method()
                else:
                    raise AttributeError(f"Method '{method_name}' not found in {self.__class__.__name__}")

        return wrapper

    return decorator


def execute_x_times_with_delay(times, delay):
    """
    A decorator that executes the decorated function `times` times
    with a `delay` (in seconds) between each execution.

    :param times: Number of times to execute the function
    :param delay: Delay in seconds between executions (default: 0)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                logger.info(f"Starting execution {i + 1} of {times}")
                func(*args, **kwargs)
                logger.info(f"Execution {i + 1}/{times} completed.")
                if i < times - 1:
                    logger.info(f"Sleeping for {delay} seconds before the next execution")
                    time.sleep(delay)  # Delay between executions in seconds
            return
        return wrapper
    return decorator
