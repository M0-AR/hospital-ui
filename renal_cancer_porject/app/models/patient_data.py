from typing import Optional, List
from datetime import date
from enum import Enum


class Gender(Enum):
    MALE = 'Male'
    FEMALE = 'Female'


class SmokingStatus(Enum):
    CURRENTLY = 'Currently'
    PREVIOUSLY = 'Previously'
    NEVER = 'Never'


class SurgicalType(Enum):
    NONE = 'None'
    LAPAROSCOPY = 'Laparoscopy'
    OPEN = 'Open'
    PARTIAL = 'Partial'


class MetastasisType(Enum):
    HISTOLOGICAL = 'Histological'
    RADIOLOGICAL = 'Radiological'


class TStage(Enum):
    TX = 'Tx'
    T1 = 'T1'
    T2 = 'T2'
    T3 = 'T3'
    T4 = 'T4'


class NStage(Enum):
    NX = 'Nx'
    N0 = 'N0'
    N1 = 'N1'


class MStage(Enum):
    MX = 'Mx'
    M0 = 'M0'
    M1 = 'M1'


class RCCSubtype(Enum):
    ccRCC = 'Clear cell carcinoma'  # Clear cell carcinoma
    non_ccRCC = 'Non-clear cell carcinoma'  # Non-clear cell carcinoma


class TreatmentType(Enum):
    SURGICAL = 'Surgical'
    ONCOLOGICAL = 'Oncological'
    SURGICAL_ONCOLOGICAL = 'Surgical + Oncological'
    NO_TREATMENT = 'No treatment'


class FuhrmanGrade(Enum):
    GRADE_1_2 = '1-2'  # Represents grades 1 to 2
    GRADE_3_4 = '3-4'  # Represents grades 3 to 4


class StageClassification(Enum):
    STAGE_I = 'I'
    STAGE_II = 'II'
    STAGE_III = 'III'
    STAGE_IV = 'IV'


class LeibovichScore(Enum):
    SCORE_0_3 = '0-3'  # Represents scores 0-3
    SCORE_4_5 = '4-5'  # Represents scores 4-5
    SCORE_ABOVE_6 = '>6'  # Represents scores >6


class SiteOfMetastasis(Enum):
    LUNG = 'Lung'
    LIVER = 'Liver'
    BONE = 'Bone'
    BRAIN = 'Brain'
    OTHER = 'Other'


class SurgicalMargin(Enum):
    POSITIVE = 'Positive'
    NEGATIVE = 'Negative'


def determine_fuhrman_grade(grade):
    if 1 <= grade <= 2:
        return FuhrmanGrade.GRADE_1_2
    elif 3 <= grade <= 4:
        return FuhrmanGrade.GRADE_3_4
    else:
        raise ValueError("Invalid Fuhrman grade value")


def determine_leibovich_score(score):
    if 0 <= score <= 3:
        return LeibovichScore.SCORE_0_3
    elif 4 <= score <= 5:
        return LeibovichScore.SCORE_4_5
    elif score > 6:
        return LeibovichScore.SCORE_ABOVE_6
    else:
        raise ValueError("Invalid Leibovich score value")


# Data Definition for each patient
class Patient:
    def __init__(self):
        self.diagnosis_date: Optional[date] = None
        self.recurrence_date: Optional[date] = None
        self.death_date: Optional[date] = None
        self.age: Optional[float] = None
        self.gender: Optional[Gender] = None
        self.bmi: Optional[float] = None
        self.symptoms: dict = {
            'haematuria': Optional[bool],
            'pain': Optional[bool],
            'weight_loss': Optional[bool],
            'other': Optional[bool]
        }
        self.smoking_status: Optional[SmokingStatus] = None
        self.asa_score: Optional[int] = None
        self.performance_status: Optional[int] = None
        self.decision_mdt: Optional[bool] = None
        self.hypertension: Optional[bool] = None
        self.fuhrman_grade: Optional[FuhrmanGrade] = None
        self.necrosis: Optional[bool] = None
        self.t_stage: Optional[TStage] = None
        self.n_stage: Optional[NStage] = None
        self.m_stage: Optional[MStage] = None
        self.stage: Optional[StageClassification] = None
        self.leibovich_score: Optional[LeibovichScore] = None
        self.sarcomatoid: Optional[bool] = None
        self.recurrence: Optional[bool] = None
        self.positive_surgical_margin: Optional[bool] = None
        self.type_of_surgery: Optional[SurgicalType] = None
        self.debulking: Optional[bool] = None
        self.lymphadenectomy: Optional[bool] = None
        self.site_of_metastasis: List[SiteOfMetastasis] = []
        self.type_of_metastasis: Optional[MetastasisType] = None
        self.treatment_type_recurrence: Optional[TreatmentType] = None
        self.ccRCC: Optional[RCCSubtype] = None
        self.non_ccRCC: Optional[RCCSubtype] = None

    def to_dict(self) -> dict:
        """
        Convert the patient data to a dictionary. This can be useful for
        converting to a DataFrame later.
        """
        return vars(self)

    # Validation for diagnosis_date
    @property
    def diagnosis_date(self) -> Optional[date]:
        return self._diagnosis_date

    @diagnosis_date.setter
    def diagnosis_date(self, value: date) -> None:
        if value is not None and not isinstance(value, date):
            raise ValueError("Diagnosis date must be a date object or None.")
        self._diagnosis_date = value

    # Validation for recurrence_date
    @property
    def recurrence_date(self) -> Optional[date]:
        return self._recurrence_date

    @recurrence_date.setter
    def recurrence_date(self, value: date) -> None:
        if value is not None and not isinstance(value, date):
            raise ValueError("Recurrence date must be a date object or None.")
        self._recurrence_date = value

    # Validation for death_date
    @property
    def death_date(self) -> Optional[date]:
        return self._death_date

    @death_date.setter
    def death_date(self, value: date) -> None:
        if value is not None and not isinstance(value, date):
            raise ValueError("Death date must be a date object or None.")
        self._death_date = value

    # Validation for age
    @property
    def age(self) -> Optional[float]:
        return self._age

    @age.setter
    def age(self, value: float) -> None:
        if value is not None and (value < 0 or value > 120):
            raise ValueError("Age must be between 0 and 120.")
        self._age = value

    # Validation for gender
    @property
    def gender(self) -> Optional[Gender]:
        return self._gender

    @gender.setter
    def gender(self, value: Gender) -> None:
        if value is not None and not isinstance(value, Gender):
            raise ValueError("Gender must be an instance of the Gender Enum or None.")
        self._gender = value

    # Validation for bmi
    @property
    def bmi(self) -> Optional[float]:
        return self._bmi

    @bmi.setter
    def bmi(self, value: float) -> None:
        if value is not None and (value < 10 or value > 100):
            raise ValueError("BMI must be between 10 and 100.")
        self._bmi = value

    # Validation for symptoms
    @property
    def symptoms(self) -> dict:
        return self._symptoms

    @symptoms.setter
    def symptoms(self, value: dict) -> None:
        if not isinstance(value, dict):
            raise ValueError("Symptoms must be a dictionary.")
        for key in ['haematuria', 'pain', 'weight_loss', 'other']:
            if key not in value or not isinstance(value[key], (bool, type(None))):
                raise ValueError(f"{key} in symptoms must be a boolean or None.")
        self._symptoms = value

    @property
    def smoking_status(self) -> Optional[SmokingStatus]:
        return self._smoking_status

    @smoking_status.setter
    def smoking_status(self, value: SmokingStatus) -> None:
        if value is not None and not isinstance(value, SmokingStatus):
            raise ValueError("Smoking status must be an instance of SmokingStatus Enum or None.")
        self._smoking_status = value

    @property
    def asa_score(self) -> Optional[int]:
        return self._asa_score

    @asa_score.setter
    def asa_score(self, value: int) -> None:
        valid_scores = [1, 2, 3, 4, 5]  # Assuming these are the valid ASA scores
        if value is not None and value not in valid_scores:
            raise ValueError("ASA score must be one of [1, 2, 3, 4, 5].")
        self._asa_score = value

    @property
    def performance_status(self) -> Optional[int]:
        return self._performance_status

    @performance_status.setter
    def performance_status(self, value: int) -> None:
        valid_statuses = [0, 1, 2, 3, 4, 5]  # Assuming these are the valid performance statuses
        if value is not None and value not in valid_statuses:
            raise ValueError("Performance status must be one of [0, 1, 2, 3, 4, 5].")
        self._performance_status = value

    @property
    def decision_mdt(self) -> Optional[bool]:
        return self._decision_mdt

    @decision_mdt.setter
    def decision_mdt(self, value: bool) -> None:
        if value is not None and not isinstance(value, bool):
            raise ValueError("Decision MDT must be a boolean or None.")
        self._decision_mdt = value

    @property
    def hypertension(self) -> Optional[bool]:
        return self._hypertension

    @hypertension.setter
    def hypertension(self, value: bool) -> None:
        if value is not None and not isinstance(value, bool):
            raise ValueError("Hypertension must be a boolean or None.")
        self._hypertension = value

    @property
    def fuhrman_grade(self) -> Optional[FuhrmanGrade]:
        return self._fuhrman_grade

    @fuhrman_grade.setter
    def fuhrman_grade(self, value: int) -> None:
        if value is not None:
            self._fuhrman_grade = determine_fuhrman_grade(value)
        else:
            self._fuhrman_grade = None

    @property
    def necrosis(self) -> Optional[bool]:
        return self._necrosis

    @necrosis.setter
    def necrosis(self, value: bool) -> None:
        if value is not None and not isinstance(value, bool):
            raise ValueError("Necrosis must be a boolean or None.")
        self._necrosis = value

    @property
    def t_stage(self) -> Optional[TStage]:
        return self._t_stage

    @t_stage.setter
    def t_stage(self, value: TStage) -> None:
        if value is not None and not isinstance(value, TStage):
            raise ValueError("T stage must be an instance of TStage Enum or None.")
        self._t_stage = value

    @property
    def n_stage(self) -> Optional[NStage]:
        return self._n_stage

    @n_stage.setter
    def n_stage(self, value: NStage) -> None:
        if value is not None and not isinstance(value, NStage):
            raise ValueError("N stage must be an instance of NStage Enum or None.")
        self._n_stage = value

    @property
    def m_stage(self) -> Optional[MStage]:
        return self._m_stage

    @m_stage.setter
    def m_stage(self, value: MStage) -> None:
        if value is not None and not isinstance(value, MStage):
            raise ValueError("M stage must be an instance of MStage Enum or None.")
        self._m_stage = value

    @property
    def stage(self) -> Optional[StageClassification]:
        return self._stage

    @stage.setter
    def stage(self, value: StageClassification) -> None:
        if value is not None and not isinstance(value, StageClassification):
            raise ValueError("Stage must be an instance of StageClassification Enum or None.")
        self._stage = value

    @property
    def leibovich_score(self) -> Optional[LeibovichScore]:
        return self._leibovich_score

    @leibovich_score.setter
    def leibovich_score(self, value: int) -> None:
        if value is not None:
            self._leibovich_score = determine_leibovich_score(value)
        else:
            self._leibovich_score = None

    @property
    def sarcomatoid(self) -> Optional[bool]:
        return self._sarcomatoid

    @sarcomatoid.setter
    def sarcomatoid(self, value: bool) -> None:
        if value is not None and not isinstance(value, bool):
            raise ValueError("Sarcomatoid must be a boolean or None.")
        self._sarcomatoid = value

    @property
    def recurrence(self) -> Optional[bool]:
        return self._recurrence

    @recurrence.setter
    def recurrence(self, value: bool) -> None:
        if value is not None and not isinstance(value, bool):
            raise ValueError("Recurrence must be a boolean or None.")
        self._recurrence = value

    @property
    def positive_surgical_margin(self) -> Optional[bool]:
        return self._positive_surgical_margin

    @positive_surgical_margin.setter
    def positive_surgical_margin(self, value: bool) -> None:
        if value is not None and not isinstance(value, bool):
            raise ValueError("Positive surgical margin must be a boolean or None.")
        self._positive_surgical_margin = value

    @property
    def type_of_surgery(self) -> Optional[SurgicalType]:
        return self._type_of_surgery

    @type_of_surgery.setter
    def type_of_surgery(self, value: SurgicalType) -> None:
        if value is not None and not isinstance(value, SurgicalType):
            raise ValueError("Type of surgery must be an instance of SurgicalType Enum or None.")
        self._type_of_surgery = value

    @property
    def debulking(self) -> Optional[bool]:
        return self._debulking

    @debulking.setter
    def debulking(self, value: bool) -> None:
        if value is not None and not isinstance(value, bool):
            raise ValueError("Debulking must be a boolean or None.")
        self._debulking = value

    @property
    def lymphadenectomy(self) -> Optional[bool]:
        return self._lymphadenectomy

    @lymphadenectomy.setter
    def lymphadenectomy(self, value: bool) -> None:
        if value is not None and not isinstance(value, bool):
            raise ValueError("Lymphadenectomy must be a boolean or None.")
        self._lymphadenectomy = value

    @property
    def site_of_metastasis(self) -> List[SiteOfMetastasis]:
        return self._site_of_metastasis

    @site_of_metastasis.setter
    def site_of_metastasis(self, value: List[SiteOfMetastasis]) -> None:
        if not all(isinstance(item, SiteOfMetastasis) for item in value):
            raise ValueError("Each item in site of metastasis must be an instance of SiteOfMetastasis Enum.")
        self._site_of_metastasis = value

    @property
    def type_of_metastasis(self) -> Optional[MetastasisType]:
        return self._type_of_metastasis

    @type_of_metastasis.setter
    def type_of_metastasis(self, value: MetastasisType) -> None:
        if value is not None and not isinstance(value, MetastasisType):
            raise ValueError("Type of metastasis must be an instance of MetastasisType Enum or None.")
        self._type_of_metastasis = value

    @property
    def treatment_type_recurrence(self) -> Optional[TreatmentType]:
        return self._treatment_type_recurrence

    @treatment_type_recurrence.setter
    def treatment_type_recurrence(self, value: TreatmentType) -> None:
        if value is not None and not isinstance(value, TreatmentType):
            raise ValueError("Treatment type for recurrence must be an instance of TreatmentType Enum or None.")
        self._treatment_type_recurrence = value

    @property
    def ccRCC(self) -> Optional[RCCSubtype]:
        return self._ccRCC

    @ccRCC.setter
    def ccRCC(self, value: RCCSubtype) -> None:
        if value is not None and not isinstance(value, RCCSubtype):
            raise ValueError("Clear cell carcinoma (ccRCC) must be an instance of RCCSubtype Enum or None.")
        self._ccRCC = value

    @property
    def non_ccRCC(self) -> Optional[RCCSubtype]:
        return self._non_ccRCC

    @non_ccRCC.setter
    def non_ccRCC(self, value: RCCSubtype) -> None:
        if value is not None and not isinstance(value, RCCSubtype):
            raise ValueError("Non-clear cell carcinoma (non-ccRCC) must be an instance of RCCSubtype Enum or None.")
        self._non_ccRCC = value
