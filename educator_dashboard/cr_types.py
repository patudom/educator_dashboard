from typing import Dict, List, Optional, Union, Any, TypedDict, cast, Protocol


class MeasurementStatus(TypedDict):
    """Type for class measurement status summary"""
    summary: Dict[str, int]
    status: Any  # Pandas DataFrame


class ShortReport(TypedDict, total=False):
    """Type for short report data structure"""
    student_id: List[int]
    username: List[str]
    name: Optional[List[str]]
    class_id: int
    progress: List[str]
    percent_story_complete: List[float]
    max_stage_index: List[int]
    max_stage_marker: List[str]
    stage_index: List[int]
    total_score: List[int]
    out_of_possible: List[int]
    Hubble_Constant: List[float]
    Age: List[float]
    last_modified: str


class QuestionInfo(TypedDict):
    """Type for question information"""
    text: str
    shorttext: str
    nicetag: str


class ClassSummary(TypedDict):
    """Type for class summary data"""
    H0: List[float]
    age: List[float]
    student_id: List[int]


class ProgressSummary(TypedDict):
    """Type for progress summary data"""
    progress: List[str]
    percent_story_complete: List[float]


class HubbleData(TypedDict):
    """Type for Hubble data calculations"""
    hubble_constant: Any  # Pandas Series
    age: Any  # Pandas Series
