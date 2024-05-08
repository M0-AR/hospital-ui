subtype_mapping = {
    "M82603": "papillært adenokarcinom",
    "M82900": "onkocytom (oksyfilt adenom)",
    "M829A1": "onkocytær tumor NOS",
    "M83103": "clear cell adenokarcinom",
    "M83113": "fumarat hydratase-deficient renalcellekarcinom",
    "M83123": "uklassificerbart renalcellekarcinom",
    "M83161": "multilokulær cystisk clear cell neoplasi, lavt malignitetspotentiale",
    "M83163": "tubulocystisk renalcellekarcinom",
    "M83173": "kromofobt renalcellekarcinom",
    "M83193": "samlerørskarcinom",
    "M831A3": "mucinøst tubulært og spindle cell karcinom",
    "M831D3": "succinat dehydrogenase-deficient renalcellekarcinom",
    "M831E3": "erhvervet cystisk nyresygdom-associeret renalcellekarcinom",
    "M831F3": "eosinofilt solidt og cystisk renalcellekarcinom",
    "M831G3": "TFE3-rearrangeret renalcellekarcinom",
    "M831H3": "TFEB-ændret renalcellekarcinom",
    "M831J3": "ELOC-muteret renalcellekarcinom",
    "M831K3": "ALK-rearrangeret renalcellekarcinom",
    "M83231": "clear cell papillær renalcelletumor",
    "M83250": "metanefrisk adenom",
    "M84803": "mucinøst adenokarcinom",
    "M84903": "Signetringscellekarcinom",
    "M73050": "onkocytær metaplasi"
}

leibovich_score_mapping = {
    "ÆF000B": "Leibovich score 0",
    "ÆF001B": "Leibovich score 1",
    "ÆF002B": "Leibovich score 2",
    "ÆF003B": "Leibovich score 3",
    "ÆF004B": "Leibovich score 4",
    "ÆF005B": "Leibovich score 5",
    "ÆF006B": "Leibovich score 6",
    "ÆF007B": "Leibovich score 7",
    "ÆF008B": "Leibovich score 8",
    "ÆF009B": "Leibovich score 9",
    "ÆF010B": "Leibovich score 10",
    "ÆF011B": "Leibovich score 11"
}

resection_range_mapping = {
    "M09400": "resektionsrande frie",
    "M09401": "resektionsrande ikke frie",
    "M09402": "resektionsrande kan ikke vurderes",
    # TODO: it was without 'e' at the end -> 'resektionsrand kan ikke vurderes' what is the correct with or without 'e'?
    "M09405": "resektionsflade fri",
    "M09406": "resektionsflade ikke fri",
    "M09407": "resektionsflade kan ikke vurderes",
    "M0940A": "resektionsafstand tilstrækkelig",
    "M0940B": "resektionsafstand ikke tilstrækkelig",
    "M0940P": "adenom i resektionsrand"
}

fuhrman_grade_mapping = {
    "ÆYYX10": "grad 1",
    "ÆYYX20": "grad 2",
    "ÆYYX30": "grad 3",
    "ÆYYX40": "grad 4",
    "ÆYYX50": "grad 5"
}

who_grade_mapping = {
    "ÆYYYH1": "WHO grad 1",
    "ÆYYYH2": "WHO grad 2",
    "ÆYYYH3": "WHO grad 3",
    "ÆYYYH4": "WHO grad 4",
    "ÆYYYH5": "WHO grad 5"
}

isup_mapping = {
    "ÆF0601": "ISUP grad 1",
    "ÆF0602": "ISUP grad 2",
    "ÆF0603": "ISUP grad 3",
    "ÆF0604": "ISUP grad 4",
    "ÆF0605": "ISUP grad 5"
}

sarkomatoid_mapping = {
    "ÆYYY0V": "sarkomatoid"
}

t_stage_mapping = {
    "ÆF1800": "pT",
    "ÆF1810": "pTis",
    "ÆF181A": "pTa",
    "ÆF1820": "pT0",
    "ÆF1830": "pT1",
    "ÆF1831": "pT1a",
    "ÆF1832": "pT1b",
    "ÆF1833": "pT1c",
    "ÆF1834": "pT1a1",
    "ÆF1835": "pT1a2",
    "ÆF1836": "pT1b1",
    "ÆF1837": "pT1b2",
    "ÆF1838": "pT1d",
    "ÆF1839": "pT1mi",
    "ÆF183A": "pT1c1",
    "ÆF183B": "pT1c2",
    "ÆF183C": "pT1c3",
    "ÆF1840": "pT2",
    "ÆF1841": "pT2a",
    "ÆF1842": "pT2b",
    "ÆF1843": "pT2c",
    "ÆF1844": "pT2d",
    "ÆF1845": "pT2a1",
    "ÆF1846": "pT2a2",
    "ÆF1850": "pT3",
    "ÆF1851": "pT3a",
    "ÆF1852": "pT3b",
    "ÆF1853": "pT3c",
    "ÆF1854": "pT3d",
    "ÆF1860": "pT4",
    "ÆF1861": "pT4a",
    "ÆF1862": "pT4b",
    "ÆF1863": "pT4c",
    "ÆF1864": "pT4d",
    "ÆF1870": "pTx"
}

n_stage_mapping = {
    "ÆF1900": "pN0",
    "ÆF1902": "pN0(i+)",
    "ÆF1903": "pN0(mol-)",
    "ÆF1904": "pN0(mol+)",
    "ÆF1905": "pN0(sn)",
    "ÆF1906": "pN0(i+)(sn)",
    "ÆF1907": "pN0(mol-)(sn)",
    "ÆF1908": "pN0(mol+)(sn)",
    "ÆF1910": "pN1",
    "ÆF1911": "pN1a",
    "ÆF1912": "pN1b",
    "ÆF1913": "pN1c",
    "ÆF1914": "pN1(mi)",
    "ÆF1915": "pN1(sn)",
    "ÆF1916": "pN1(mi)(sn)",
    "ÆF1917": "pN1a(sn)",
    "ÆF1918": "pN1b(sn)",
    "ÆF1919": "pN1c(sn)",
    "ÆF1920": "pN2",
    "ÆF1921": "pN2a",
    "ÆF1922": "pN2b",
    "ÆF1923": "pN2(sn)",
    "ÆF1924": "pN2a(sn)",
    "ÆF1925": "pN2b(sn)",
    "ÆF1930": "pN3",
    "ÆF1931": "pN3a",
    "ÆF1932": "pN3b",
    "ÆF1933": "pN3c",
    "ÆF1940": "pN4",
    "ÆF1950": "pNx"
}

m_stage_mapping = {
    "ÆF2000": "pM0",
    "ÆF2001": "pM0(i+)",
    "ÆF2004": "pM0(mol+)",
    "ÆF2010": "pM1",
    "ÆF2011": "pM1a",
    "ÆF2012": "pM1b",
    "ÆF2013": "pM1c",
    "ÆF2014": "pM1d",
    "ÆF2050": "pMx"
}

nekroser_mapping = {
    "M54000": "nekrose"
}

mappings = {
    "Subtype": subtype_mapping,
    "LeibovichScore": leibovich_score_mapping,
    "ResectionRange": resection_range_mapping,
    "FuhrmanGrade": fuhrman_grade_mapping,
    "WHOScore": who_grade_mapping,
    "ISUPGrade": isup_mapping,
    "Sarkomatoid": sarkomatoid_mapping,
    "TStage": t_stage_mapping,
    "NStage": n_stage_mapping,
    "MStage": m_stage_mapping,
    "Nekroser": nekroser_mapping
}
