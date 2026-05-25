from sqlalchemy import text, BigInteger, DateTime, Date, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from datetime import datetime, date
from typing import Annotated

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
date_utc = Annotated[datetime, mapped_column(
        DateTime(timezone=True),
        server_default=text("(CURRENT_TIMESTAMP + '03:00:00'::interval)")
    )]
str_100 = Annotated[str, String(100)]
str_50 = Annotated[str, String(50)]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_100: String(100),
        str_50: String(50)
    }


class ApplicantsModel(Base):
    __tablename__ = "applicants"
    __table_args__ = {"schema": "reg_office"}

    applicantid: Mapped[intpk]
    surname: Mapped[str_100] = mapped_column(nullable=False)
    name: Mapped[str_100] = mapped_column(nullable=False)
    middlename: Mapped[str_100] = mapped_column(nullable=False)
    passportnumber: Mapped[str] = mapped_column(String(8), nullable=False)
    phonenumber: Mapped[str] = mapped_column(String(11), nullable=False)
    registration_address: Mapped[str_50] = mapped_column(String(50))


class ApplicationsModel(Base):
    __tablename__ = "applications"
    __table_args__ = {"schema": "reg_office"}

    applicationid: Mapped[intpk]
    citizenid: Mapped[int] = mapped_column(
        ForeignKey('citizens.citizenid'),
        nullable=False)
    applicantid: Mapped[int] = mapped_column(
        ForeignKey('applicants.applicantid'),
        nullable=False)
    staffid: Mapped[int] = mapped_column(
        ForeignKey('staff.staffid'))
    dateofapplication: Mapped[date_utc]
    kindofapplication: Mapped[str] = mapped_column(String(50), nullable=False)
    statusofapplication: Mapped[str] = mapped_column(String(50), nullable=False, server_default='under consideration')
    channel: Mapped[str] = mapped_column(String(7))
    from_draft: Mapped[bool] = mapped_column()


class BirthCertificatesModel(Base):
    __tablename__ = 'birthcertificates'
    __table_args__ = {"schema": "reg_office"}

    birthcertificateid: Mapped[intpk]
    citizenid: Mapped[int] = mapped_column(
        ForeignKey('citizens.citizenid'),
        nullable=False
    )
    placeofbirth: Mapped[str] = mapped_column(String(100), nullable=False)
    mother: Mapped[str] = mapped_column(String(20), nullable=False)
    father: Mapped[str] = mapped_column(String(50), nullable=False)
    grandma: Mapped[str] = mapped_column(String(50))
    grandpa: Mapped[str] = mapped_column(String(50))


class CitizensModel(Base):
    __tablename__ = 'citizens'
    __table_args__ = {"schema": "reg_office"}

    citizenid: Mapped[intpk]
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    middlename: Mapped[str] = mapped_column(String(100), nullable=False)
    passportnumber: Mapped[str] = mapped_column(String(8))
    dateofbirth: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    image: Mapped[str] = mapped_column(String(100))
    registration_address: Mapped[str] = mapped_column(String(50))


class DeathCertificatesModel(Base):
    __tablename__ = 'deathcertificates'
    __table_args__ = {"schema": "reg_office"}

    deathcertificateid: Mapped[intpk]
    citizenid: Mapped[int] = mapped_column(
        ForeignKey('citizens.citizenid'),
        nullable=False
    )
    dateofdeath: Mapped[str] = mapped_column(nullable=False)
    placeofdeath: Mapped[str] = mapped_column(String(50), nullable=False)

# c date (Date) ???
class DocRequestsModel(Base):
    __tablename__ = 'doc_requests'
    __table_args__ = {"schema": "reg_office"}

    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(70), nullable=False)
    created: Mapped[date] = mapped_column(Date, nullable=False)
    appid: Mapped[int] = mapped_column(

        nullable=False
    )
    error: Mapped[str] = mapped_column()
    id: Mapped[intpk]
    docfile: Mapped[str] = mapped_column()
    is_sent: Mapped[bool] = mapped_column()
    updated: Mapped[date] = mapped_column(Date)


class DraftsModel(Base):
    __tablename__ = 'drafts'
    __table_args__ = {"schema": "reg_office"}

    id: Mapped[intpk]
    dateofapplication: Mapped[date_utc]
    kindofapplication: Mapped[str] = mapped_column(String(50), nullable=False)
    statusofapplication: Mapped[str] = mapped_column(String(50), nullable=False, server_default='draft')
    applicant_name: Mapped[str] = mapped_column()
    applicant_surname: Mapped[str] = mapped_column()
    applicant_middlename: Mapped[str] = mapped_column()
    applicant_passport: Mapped[str] = mapped_column()
    applicant_phone: Mapped[str] = mapped_column()
    applicant_registration_address: Mapped[str] = mapped_column()
    citizen_name: Mapped[str] = mapped_column()
    citizen_surname: Mapped[str] = mapped_column()
    citizen_middlename: Mapped[str] = mapped_column()
    citizen_passport: Mapped[str] = mapped_column()
    citizen_birthdate: Mapped[str] = mapped_column()
    citizen_gender: Mapped[str] = mapped_column()
    birth_place: Mapped[str] = mapped_column()
    birth_mother: Mapped[str] = mapped_column()
    birth_father: Mapped[str] = mapped_column()
    death_date: Mapped[str] = mapped_column()
    death_place: Mapped[str] = mapped_column()
    marriage_date: Mapped[str] = mapped_column()
    marriage_surname: Mapped[str] = mapped_column()
    marriage_newsurname: Mapped[str] = mapped_column()
    marriage_name: Mapped[str] = mapped_column()
    marriage_middlename: Mapped[str] = mapped_column()
    marriage_passport: Mapped[str] = mapped_column()
    marriage_birthdate: Mapped[str] = mapped_column()
    channel: Mapped[str] = mapped_column()
    app_id: Mapped[int] = mapped_column(BigInteger)


class MerrigeCertificatesModel(Base):
    __tablename__ = 'merrigecertificates'
    __table_args__ = {"schema": "reg_office"}

    merrigecertificateid: Mapped[intpk]
    citizenid: Mapped[int] = mapped_column(
        ForeignKey('citizens.citizenid'),
        nullable=False
    )
    dateofmerrige: Mapped[date] = mapped_column(Date, nullable=False)
    surnameofspouse: Mapped[str] = mapped_column(String(50), nullable=False)
    newsurnameofspouse: Mapped[str] = mapped_column(String(50))
    nameofspouse: Mapped[str] = mapped_column(String(20), nullable=False)
    middlenameofspouse: Mapped[str] = mapped_column(String(20), nullable=False)
    passportnumberofspouse: Mapped[str] = mapped_column(String(8), nullable=False)
    dateofbirthofspouse: Mapped[date] = mapped_column(Date, nullable=False)

# class PushTokensModel(Base):
#     __tablename__ = 'pushtokens'
#
#     id: Mapped[int] = mapped_column(nullable=False)
#     push_token_id: Mapped[str] = mapped_column(String(300), nullable=False)
#     date: Mapped[str] = mapped_column(String(100), nullable=False)
#     device_info: Mapped[str] = mapped_column(String(1000))


# class SettingsModel(Base):
#     __tablename__ = 'settings'
#
#     name: Mapped[str] = mapped_column(nullable=False)
#     value: Mapped[str] = mapped_column()
#     id: Mapped[int] = mapped_column(nullable=False)

class StaffModel(Base):
    __tablename__ = 'staff'
    __table_args__ = {"schema": "reg_office"}

    staffid: Mapped[intpk]
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    middlename: Mapped[str] = mapped_column(String(100), nullable=False)
    dateofbirth: Mapped[date] = mapped_column(Date, nullable=False)
    passportnumber: Mapped[str] = mapped_column(String(8), nullable=False)
    phonenumber: Mapped[str] = mapped_column(String(11), nullable=False)