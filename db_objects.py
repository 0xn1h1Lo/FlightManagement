from dataclasses import astuple, dataclass, fields, is_dataclass
from datetime import date, datetime

def pprint_db_objects(objects):
    '''Prints a list of db_objects as a table'''
    if not objects:
        print("No Record")
        return
    first = objects[0]
    
    headers = [field.name for field in fields(first)]
    rows = [[str(value) for value in astuple(object)] for object in objects]
    pprint_table(rows, headers)

def pprint_table(rows, headers = []):
    width = [len(header) for header in headers] if headers else [0 for row in rows]
    # Keeping the longest string in each column
    for row in rows:
        for i, cell in enumerate(row):
            width[i] = max(width[i], len(str(cell)))

    print(" | ".join(header.ljust(width[i]) for i, header in enumerate(headers)))  # generator centering header in each cell based on width
    print(" + ".join("-" * width[i] for i in range(len(headers))))  # generator yielding "----" of the length of each value in width
    for row in rows:
        print(" | ".join(str(cell).ljust(width[i]) for i, cell in enumerate(row)))  # same as header, converting cell to string to call ljust on it

# skips are the fields to skip when prompting
def make_object(cls):
    '''Create a db_object for insertion into the database based on user input'''
    skips = getattr(cls, "skips", [])  # prompt can skip optional fields if set
    values = dict()
    for i, field in enumerate(fields(cls)):
        if i in skips:
            continue
        values[field.name] = input(f"> Please enter a value for {field.name} ({field.type.__name__}): ")

    return cls(**values)

def list_headers(cls):
    print(" ".join(f"[{field.name}]" for field in fields(cls)))

# fields in the dataclasses below must match in order and number 
# with the columns in SELECT statements in schema.sql
# the name could be changed here for nicer display

## VIEWS

@dataclass
class Pilot:
    table = "PilotsView"

    pil_id: str
    flying_time_min: int
    first_name: str
    last_name: str
    DOB: date
    email: str
    phone_num: str
    model: str

    def sql_ready(self):
        res = dict()
        # only add in people and pilots if we are not just adding a certification
        if not all(field == "" for field in astuple(self)[1:-1]):
            res["people"] = (self.pil_id, self.first_name, self.last_name, self.DOB, self.email, self.phone_num)
            res["pilots"] = (self.pil_id, self.flying_time_min)
        # do not add certification is the value is the empty string
        if self.model:
            res["certifications"] = (self.pil_id, self.model)
        return res

@dataclass
class Manifest:
    table = "ManifestsView"

    man_id: int
    pil_id: int
    pil_first_name: str
    pil_last_name: str
    pil_fly_time_min: int
    copil_id: int
    copil_first_name: str
    copil_last_name: str
    copil_fly_time_min: int

@dataclass
class Destination:
    table = "DestinationsView"

    airport_code: str
    latitude: float
    longitude: float
    parking_location: str

    def sql_ready(self):
        res = dict()
        res["destinations"] = (self.airport_code, self.latitude, self.longitude, self.parking_location)
        return res

@dataclass
class Plane:
    table = "PlanesView"

    reg: str
    model: str
    capacity_kg: int
    range_km: int
    airspeed_kmh: int

    def sql_ready(self):
        res = dict()
        res["plane_models"] = (self.model, self.capacity_kg, self.range_km, self.airspeed_kmh)
        res["planes"] = (self.reg, self.model)
        return res

@dataclass
class Flight:
    table = "FlightsView"
    skips = [9, 10, 11, 12]  # normal attribute, not included as a field

    fli_date: date  # before storing use isoformat()
    fli_num: str
    fli_status: str
    leg_id: int
    orig: str
    dest: str
    reg: str
    man_id: int
    STD: datetime  # before storing use isoformat(sep= " ")
    ATA: str = None
    pil_id: int = None
    copil_id: int = None
    model: str = None

    def sql_ready(self):
        res = dict()
        res["flights"] = (self.fli_date, self.fli_num, self.fli_status)
        res["legs"] = (self.fli_date, self.fli_num, self.leg_id, self.orig, self.dest, self.reg, self.man_id, self.STD, self.ATA)  # ATA is null
        return res

## BASE TABLES
# Write directly to the tables without getting prompted for each unsused attribute of the view

@dataclass
class people:
    table = "people"

    person_id: str
    first_name: str
    last_name: str
    DOB: date
    email: str
    phone_num: str

@dataclass
class plane_models:
    table = "plane_models"

    model: str
    capacity_kg: int
    range_km: int
    airspeed_kmh: int  

@dataclass
class destinations:
    table = "destinations"

    airport_code: str
    latitude: float
    longitude: float
    parking_location: str  

@dataclass
class flights:
    table = "flights"

    fli_date: int
    fli_num: str
    fli_status: str

@dataclass
class pilots:
    table = "pilots"

    pil_id: str
    flying_time_min: int

@dataclass
class planes:
    table = "planes"

    reg: str
    model: str

@dataclass
class crew:
    table = "crew"

    crew_id: int
    role: str

@dataclass
class certifications:
    table = "certifications"

    pil_id: int
    model: str

@dataclass
class manifests:
    table = "manifests"

    man_id: int
    pil_id: int
    copil_id: int

    def sql_ready(self):
        return {type(self).__name__: astuple(self)}
    
@dataclass
class crew_manifests:
    table = "crew_manifests"

    c_man_id: int
    crew_id: int

@dataclass
class passenger_manifests:
    table = "passenger_manifests"

    p_man_id: int
    person_id: int

@dataclass
class legs:
    table = "legs"

    fli_date: int
    fli_num: str
    leg_id: int
    orig: str
    dest: str
    reg: str
    man_id: int
    STD: int
    ATA: int 