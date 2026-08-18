from enum import IntEnum

class EventStatus(IntEnum):
  Created = 0
  Planning = 1
  RegistrationOpen = 2
  RegistrationClosed = 3
  Completed = 4
  Closed = 5
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]
  

class Gender(IntEnum):
  notDefined = 0
  male = 1
  female = 2 
  others = 3

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]
  
class SponsorCategory(IntEnum):
  notDefined = 0
  Primary = 1
  Secondary = 2
  Tertiary = 3
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]


class OrganisationStatus(IntEnum):
  Active = 0
  Inactive = 1

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]


class OrganisationMemberStatus(IntEnum):
  Active = 0
  Inactive = 1
  Pending = 2
  expired = 3
  rejected = 4
  cancelled = 5
  suspended = 6
  terminated = 7
  onhold = 8

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]


class OrganisationMemberRole(IntEnum):
  Member = 0
  Admin = 1
  Secretary = 2
  Director = 3
  Owner = 4

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]


class OrganisationType(IntEnum):
  International = 0
  National = 1
  Regional = 2
  SubRegional = 3
  Association = 4
  Club = 5

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]

class ClubStatus(IntEnum):
  Active = 0
  Inactive = 1

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]

class ClubMemberStatus(IntEnum):
  Active = 0
  Inactive = 1
  Pending = 2

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]


class ClubMemberRole(IntEnum):
  Member = 0
  Admin = 1
  Secretary = 2
  Director = 3
  Owner = 4

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]


class SubscriberType(IntEnum):
  Participant = 0
  Organisation = 1

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]


class BillingFrequency(IntEnum):
  Monthly = 0
  Annual = 1
  OnceOff = 2

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]


class SubscriptionStatus(IntEnum):
  Pending = 0
  Trial = 1
  Active = 2
  Suspended = 3
  Expired = 4
  Cancelled = 5

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]