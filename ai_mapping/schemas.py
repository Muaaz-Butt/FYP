from pydantic import BaseModel, Field
from typing import List, Optional

class FieldMapping(BaseModel):
    selector: str = Field(description="CSS selector, e.g., #first_name")
    type: str = Field(description="Input type, e.g., text, email, select")
    value: str = Field(description="The data from the student's profile to insert")
    confidence: float = Field(description="AI confidence score between 0 and 1")

class AutomationStep(BaseModel):
    action: str = Field(description="The action: 'fill', 'click', or 'submit'")
    selector: Optional[str] = Field(None, description="Selector for button or form")
    fields: Optional[List[FieldMapping]] = Field(None, description="Fields to fill in this step")

class AutomationResponse(BaseModel):
    application_id: int
    url: str
    steps: List[AutomationStep]