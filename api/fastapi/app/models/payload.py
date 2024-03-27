from typing import List
from pydantic import BaseModel

# ['day_of_week','gametime_hr','away_team','TeamId','Division','StadiumType','gametime_hr']
# ['Capacity','week_num', 'division_game','arrests']

class NFLArrestPredictionPayload(BaseModel):
    week_num: int
    capacity: int
    division_game: int
    day_of_week: str
    home_team: str
    away_team: str
    home_team_abbrv: str
    away_team: str
    division: str
    stadium_type: str
    gametime_hr: str

def payload_categorical_to_list(NFLArrestsPayload: NFLArrestPredictionPayload) -> List:
    return [
        NFLArrestsPayload.day_of_week,
        NFLArrestsPayload.home_team,
        NFLArrestsPayload.away_team,
        NFLArrestsPayload.home_team_abbrv,
        NFLArrestsPayload.division,
        NFLArrestsPayload.stadium_type,
        NFLArrestsPayload.gametime_hr
        ]

def payload_numerical_to_list(NFLArrestsPayload: NFLArrestPredictionPayload) -> List:
    return [
        
        NFLArrestsPayload.capacity,
        NFLArrestsPayload.week_num,
        NFLArrestsPayload.division_game
        ]

def payload_continuous_to_list(NFLArrestsPayload: NFLArrestPredictionPayload) -> List:
    # there are no continuous variables in this model
    return []



def payload_to_list(NFLArrestsPayload: NFLArrestPredictionPayload) -> List:
    return [
        NFLArrestsPayload.week_num,
        NFLArrestsPayload.capacity,
        NFLArrestsPayload.division_game,
        NFLArrestsPayload.day_of_week,
        NFLArrestsPayload.home_team,
        NFLArrestsPayload.home_team_abbrv,
        NFLArrestsPayload.away_team,
        NFLArrestsPayload.division,
        NFLArrestsPayload.stadium_type,
        NFLArrestsPayload.gametime_hr
        ]