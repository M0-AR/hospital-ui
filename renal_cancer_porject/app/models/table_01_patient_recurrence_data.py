from renal_cancer_porject.app.models.patient_data import Patient
from typing import Optional, Dict


class PatientRecurrenceData(Patient):
    def __init__(self):
        super().__init__()
        self._charlson_score: Optional[int] = None
        self._tumor_size: Optional[float] = None
        self.biochemistry: Dict[str, Optional[float]] = {
            'crp': None,
            'leukocyte': None,
            'neutrophilia': None,
            'sedimentation_rate': None,
            'hb': None
        }

    @property
    def charlson_score(self) -> Optional[int]:
        return self._charlson_score

    @charlson_score.setter
    def charlson_score(self, value: int) -> None:
        if value is not None and (value < 0 or value > 5):
            raise ValueError("Charlson score must be between 0 and 5.")
        self._charlson_score = value

    @property
    def tumor_size(self) -> Optional[float]:
        return self._tumor_size

    @tumor_size.setter
    def tumor_size(self, value: float) -> None:
        if value is not None and value < 0:
            raise ValueError("Tumor size must be a non-negative value.")
        self._tumor_size = value

    def set_biochemistry_value(self, key: str, value: float) -> None:
        if key not in self.biochemistry:
            raise KeyError(f"{key} is not a valid biochemistry parameter.")
        if value is not None and value < 0:
            raise ValueError(f"{key} value must be non-negative.")
        self.biochemistry[key] = value

    # Example of a method to validate and update the symptoms
    def update_symptom(self, symptom: str, value: bool) -> None:
        if symptom not in self.symptoms:
            raise KeyError(f"{symptom} is not a recognized symptom.")
        self.symptoms[symptom] = value
