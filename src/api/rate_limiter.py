from typing import Optional, Callable, Any

from fastapi import Depends, Request, HTTPException
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from limits import parse
from slowapi.util import get_remote_address
from config import redis_url


# class DynamicLimiter(Limiter):
#     def __init__(self, key_func, *args, **kwargs):
#         super().__init__(key_func, *args, **kwargs)
#         self.key_func = key_func

#     def _check_request_limit(
#         self,
#         request: Request,
#         endpoint_func: Optional[Callable[..., Any]],
#         in_middleware: bool = True,
#     ) -> None:

#         permissions = request.state.permissions
#         rate_limit_str = permissions.get('rate_limit', "10/minute")
#         rate_limit = parse(rate_limit_str)

#         self.limiter.hit(rate_limit, self.key_func(request))
#         if not self.limiter.test(rate_limit, self.key_func(request)):
#             raise HTTPException(
#                 status_code=429, detail=f"Too many requests, you get {rate_limit}"
#             )

#         return super()._check_request_limit(request, endpoint_func, in_middleware)


# def get_index_id(request: Request = Depends(Request)):
#     return request.state.index_id


# limiter = DynamicLimiter(
#     key_func=get_index_id,
#     storage_uri=redis_url
# )

anon_limiter = Limiter(key_func=get_remote_address)
