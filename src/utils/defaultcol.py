import uuid
import datetime
from sqlalchemy import String, Boolean, Column, DateTime


def get_id():
	return str(uuid.uuid4())


class DefaultColumns():
	id = Column(String, primary_key = True, default = get_id)
	is_deleted = Column(Boolean, default = False)
	created_at = Column(DateTime, default = datetime.datetime.utcnow)
	updated_at = Column(DateTime, default = datetime.datetime.utcnow,
							onupdate = datetime.datetime.utcnow)
	def update_fields(self, update: dict):
		for key, value in update.items():
			if value:
				setattr(self, key, value)