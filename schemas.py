from pydantic import BaseModel, Field
from typing import Optional, List

class ExtractedEntities(BaseModel):
    """
    Schema for extracting diagnostic parameters from vague driver input.
    """
    detected_fault_codes: List[str] = Field(
        default_factory=list,
        description="OBD-II (e.g., P0300) or BMW-specific Hex codes (e.g., 30FF) found in the text."
    )
    symptom_category: Optional[str] = Field(
        default=None,
        description="The category of the problem such as 'noise', 'leak', 'rough_idle', 'power_loss'."
    )
    operating_condition: Optional[str] = Field(
        default=None,
        description="When the issue occurs such as 'cold_start', 'idle', 'acceleration', 'braking'."
    )
    perceived_location: Optional[str] = Field(
        default=None,
        description="Where the driver thinks the issue is coming from, such as 'engine_bay', 'wheels', 'exhaust'."
    )