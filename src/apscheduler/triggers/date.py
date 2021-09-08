from __future__ import annotations

from datetime import datetime
from typing import Optional

import attr

from ..abc import Trigger
from ..marshalling import marshal_date, unmarshal_date
from ..validators import as_aware_datetime, require_state_version


@attr.define
class DateTrigger(Trigger):
    """
    Triggers once on the given date/time.

    :param run_time: the date/time to run the job at
    """

    run_time: datetime = attr.field(converter=as_aware_datetime)
    _completed: bool = attr.field(init=False, eq=False, default=False)

    def next(self) -> Optional[datetime]:
        if not self._completed:
            self._completed = True
            return self.run_time
        else:
            return None

    def __getstate__(self):
        return {
            'version': 1,
            'run_time': marshal_date(self.run_time),
            'completed': self._completed
        }

    def __setstate__(self, state):
        require_state_version(self, state, 1)
        self.run_time = unmarshal_date(state['run_time'])
        self._completed = state['completed']

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.run_time}')"
