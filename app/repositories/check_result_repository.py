from ..models.check_result_model import CheckResult

class CheckResultRepository:
    def save_result(self, db, url_id, status, response_time):
        result = CheckResult(
            url_id=url_id,
            status=status,
            response_time=response_time
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        return result