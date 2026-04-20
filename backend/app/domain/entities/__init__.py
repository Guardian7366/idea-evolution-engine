from datetime import datetime

class DateHelper:
    """
    Helper class to parse date strings coming from the database (created_at, updated_at)
    and convert them to datetime objects.
    """
    def __post_init__(self):
        if hasattr(self, 'created_at') and isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)
        if hasattr(self, 'updated_at') and isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(self.updated_at)
