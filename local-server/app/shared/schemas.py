from pydantic import BaseModel, ConfigDict


# ORM 객체의 속성으로 응답을 구성하며 model_ 접두사 필드도 허용하는 공통 스키마
class OrmModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())  # ORM 속성 변환 및 예약 접두사 정책
