



class AuthenticationFailed():
    status_code = 401
    default_detail = 'Incorrect authentication credentials.'
    default_code = 'authentication_failed'


class NotAuthenticated():
    status_code = 401
    default_detail = 'Authentication credentials were not provided.'
    default_code = 'not_authenticated'


class PermissionDenied():
    status_code = 403
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'permission_denied'


class NotFound():
    status_code = 404
    default_detail = 'Not found.'
    default_code = 'not_found'