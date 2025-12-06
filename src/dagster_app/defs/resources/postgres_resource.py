from pathlib import Path
from typing import Literal

import dagster as dg
from sqlalchemy import Engine, create_engine, text  # Util
from sqlalchemy.orm import sessionmaker  # Util


class PostgresResource(dg.ConfigurableResource):
    """
    Universal Postgres resource backed by a SQLAlchemy Engine.
    Swaps easily between local dev, self-hosted Dagster, and Dagster Cloud.
    """

    pg_port: int = 5432
    user: str
    password: str
    host: str
    db_name: str

    sslmode: str | None = None

    # Pool tuning
    pool_size: int = 5
    max_overflow: int = 10
    pool_recycle: int | None = 1800
    pool_timeout: int | None = 30

    _engine: Engine | None = None
    _SessionLocal: sessionmaker | None = None

    @property
    def db_engine(self) -> Engine:
        if self._engine is None:
            raise RuntimeError("Engine not initialized. Did Dagster spin up the resource?")
        return self._engine

    def get_session(self):
        if self._SessionLocal is None:
            raise RuntimeError("Sessionmaker not initialised.")
        return self._SessionLocal()

    # ---------- Dagster hooks ----------
    def setup_for_execution(self, _ctx: dg.InitResourceContext):
        # Build the SQLAlchemy URL
        url = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.pg_port}/{self.db_name}"

        # Create the engine with pooling options
        self._engine = create_engine(
            url,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_recycle=self.pool_recycle,
            pool_timeout=self.pool_timeout,
            connect_args={"sslmode": self.sslmode} if self.sslmode else {},
        )

        self._SessionLocal = sessionmaker(bind=self._engine, autoflush=False)

    def teardown_after_execution(self, _ctx: dg.InitResourceContext):
        if self._engine is not None:
            self._engine.dispose()

    def execute_script(self, script_folder: Literal["tables", "upserts"], script_name: str) -> None:
        """
        Executes a SQL script that can be found in the sql_scripts folder withing the data_platform
        repository.

        script_folder (Literal['tables', 'upserts']): the sub folder where the script can be found
        script_name (str): the name of the script to be executed, should include the .sql suffix
        """
        try:
            script_path = Path(__file__).parents[2] / script_folder / script_name
            sql = script_path.read_text()
            stmt = text(sql)

            with self.db_engine.connect() as conn:
                with conn.begin():
                    conn.execute(stmt)

        except FileNotFoundError as err:
            raise FileNotFoundError(
                f"""Could not find file `{script_name}` in folder `{script_folder}`. Path tried:\n
                {Path(__file__).parents[2] / script_folder / script_name}"""
            ) from err


@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "pg_resource": PostgresResource(
                user=dg.EnvVar("PG_USER"),
                password=dg.EnvVar("PG_PASSWORD"),
                host=dg.EnvVar("PG_HOST"),
                db_name="nl_app",
            )
        }
    )
