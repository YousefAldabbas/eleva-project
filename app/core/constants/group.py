from app.core.enums.group import Group
from app.models import Candidate, User

group_maper = {Group.CANDIDATE: Candidate, Group.USER: User}
