from flask import request

from infrastructure.api.resources.base import BaseResource


class StatusResource(BaseResource):
    path = '/'

    @staticmethod
    def get():
        svc = request.services["status"]
        message = {
            "Build Commit": svc.get_build_commit(),
            "Build Time": svc.get_build_time()
        }
        return message
