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


def super_admin_required(func):
    """Super admin required decorator."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Check is current user is a super admin."""
        if current_user.is_superadmin:
            return func(*args, **kwargs)
        else:
            return login_manager.unauthorized()

    return wrapper
