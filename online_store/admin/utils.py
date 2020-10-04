from flask_login import current_user
from online_store import login_manager
from functools import wraps


def admin_required(func):
    """Admin required decorator."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Check is current user is an admin."""
        if current_user.is_admin:
            return func(*args, **kwargs)
        else:
            return login_manager.unauthorized()

    return wrapper


def employee_required(func):
    """Super admin required decorator."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Check is current user is a employee."""
        if current_user.is_employee:
            return func(*args, **kwargs)
        else:
            return login_manager.unauthorized()

    return wrapper
