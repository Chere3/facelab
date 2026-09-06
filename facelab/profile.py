"""Perfil demográfico declarado por el usuario."""
from __future__ import annotations
from dataclasses import dataclass, asdict

SEXES = ["male", "female"]
ANCESTRIES = ["asian", "black", "caucasian", "hispanic", "indian", "mideastern", "other"]


@dataclass
class Profile:
    sex: str | None = None          # male | female
    ancestry: str | None = None     # ver ANCESTRIES; "other" usa normas de todo el sexo
    age: int | None = None
    ambition: str | None = None     # auto | mantenimiento | mejora | glow-up (nivel mínimo pedido por el usuario)

    def norm_keys(self) -> tuple[str | None, str | None]:
        a = None if self.ancestry in (None, "other") else self.ancestry
        return self.sex, a

    def to_dict(self):
        return asdict(self)
