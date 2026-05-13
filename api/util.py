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