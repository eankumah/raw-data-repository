from protorpc import messages
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UnicodeText, UniqueConstraint
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship

from rdr_service.model.base import Base
from rdr_service.model.utils import Enum, UTCDateTime


class CodeType(messages.Enum):
    """A type of code"""

    MODULE = 1
    TOPIC = 2
    QUESTION = 3
    ANSWER = 4


class CodeBook(Base):
    """A book of codes.

  Code books contain a list of codes that are referenced in questionnaire concepts,
  questionnaire questions, and questionnaire response answers. They are also used in participant
  summaries and metrics, in place of where an enum field might go otherwise.

  Each import of a code book gets a new ID. All codes that were already in the database are updated
  to have the new code book ID and attributes specified in the code book. Any codes in the code
  book that are missing from the database are inserted. Existing codes that are not in the code
  book are left untouched.
  """

    __tablename__ = "code_book"
    codeBookId = Column("code_book_id", Integer, primary_key=True)
    created = Column("created", UTCDateTime, nullable=False)
    # True if this is the latest imported code book.
    latest = Column("latest", Boolean, nullable=False)
    name = Column("name", String(80), nullable=False)
    system = Column("system", String(255), nullable=False)
    version = Column("version", String(80), nullable=False)
    __table_args__ = (UniqueConstraint("system", "version"),)


class _CodeBase(object):
    """Mixin with shared columns for Code and CodeHistory"""

    codeId = Column("code_id", Integer, primary_key=True)
    system = Column("system", String(255), nullable=False)
    """
    @rdr_dictionary_show_unique_values
    """
    value = Column("value", String(80), nullable=False)
    # OMOP codes can be any length according to OHDSI:
    # https://ohdsi.github.io/CommonDataModel/dataModelConventions.html#general
    # "Precision is provided only for VARCHAR. It reflects the minimal required string length
    # and can be expanded within a CDM instantiation."
    #
    # Leaving shortValue field and functionality in for any downstream users, but no longer using it in curation ETL.
    shortValue = Column("short_value", String(50))
    display = Column("display", UnicodeText)
    topic = Column("topic", UnicodeText)
    codeType = Column("code_type", Enum(CodeType), nullable=False)
    mapped = Column("mapped", Boolean, nullable=False)
    created = Column("created", UTCDateTime, nullable=False)

    @declared_attr
    def codeBookId(cls):
        return Column("code_book_id", Integer, ForeignKey("code_book.code_book_id"))

    @declared_attr
    def parentId(cls):
        return Column("parent_id", Integer, ForeignKey("code.code_id"))


class Code(_CodeBase, Base):
    """A code for a module, question, or answer.

  Questions have modules for parents, and answers have questions for parents.
  """

    __tablename__ = "code"

    @declared_attr
    def children(cls):
        return relationship(
            cls.__name__, backref=backref("parent", remote_side="Code.codeId"), cascade="all, delete-orphan"
        )

    __table_args__ = (UniqueConstraint("system", "value"),)


class CodeHistory(_CodeBase, Base):
    """A version of a code.

  New versions are inserted every time a code book is imported.

  At the moment, CodeHistory is not exposed by any endpoints, and is intended as a historical
  record of codes in case we need it in future.
  """

    __tablename__ = "code_history"

    # Since codeBookId is nullable, it can't be a part of the primary key; instead create a
    # separate PK for CodeHistory.
    codeHistoryId = Column("code_history_id", Integer, primary_key=True)
    codeId = Column("code_id", Integer)

    __table_args__ = (UniqueConstraint("code_book_id", "system", "value"), UniqueConstraint("code_book_id", "code_id"))
