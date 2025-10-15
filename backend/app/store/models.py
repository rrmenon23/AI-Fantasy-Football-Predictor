from sqlalchemy.orm import declarative_base, Mapped, mapped_column


class Team(Base):
    __tablename__ = "teams"
    team_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(8))
    name: Mapped[str] = mapped_column(String(64))
    city: Mapped[str] = mapped_column(String(64))

class Player(Base):
    __tablename__ = "players"
    player_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    team: Mapped[str] = mapped_column(String(8))
    position: Mapped[str] = mapped_column(String(8))
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class Game(Base):
    __tablename__ = "games"
    game_key: Mapped[str] = mapped_column(String(32), primary_key=True)
    season: Mapped[int] = mapped_column(Integer)
    week: Mapped[int] = mapped_column(Integer)
    date_utc: Mapped[DateTime]
    home_team: Mapped[str] = mapped_column(String(8))
    away_team: Mapped[str] = mapped_column(String(8))


class PlayerWeek(Base):
    __tablename__ = "player_week"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(Integer)
    game_key: Mapped[str] = mapped_column(String(32))
    season: Mapped[int] = mapped_column(Integer)
    week: Mapped[int] = mapped_column(Integer)
    team: Mapped[str] = mapped_column(String(8))
    opp: Mapped[str] = mapped_column(String(8))
    position: Mapped[str] = mapped_column(String(8))
    pass_yds: Mapped[float] = mapped_column(Float, default=0)
    pass_td: Mapped[float] = mapped_column(Float, default=0)
    interceptions: Mapped[float] = mapped_column(Float, default=0)
    rush_att: Mapped[float] = mapped_column(Float, default=0)
    rush_yds: Mapped[float] = mapped_column(Float, default=0)
    rush_td: Mapped[float] = mapped_column(Float, default=0)
    targets: Mapped[float] = mapped_column(Float, default=0)
    receptions: Mapped[float] = mapped_column(Float, default=0)
    rec_yds: Mapped[float] = mapped_column(Float, default=0)
    rec_td: Mapped[float] = mapped_column(Float, default=0)
    fumbles_lost: Mapped[float] = mapped_column(Float, default=0)
    ppr: Mapped[float] = mapped_column(Float, default=0)
    half_ppr: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[DateTime]
    __table_args__ = (UniqueConstraint("player_id","season","week", name="uq_player_week"),)