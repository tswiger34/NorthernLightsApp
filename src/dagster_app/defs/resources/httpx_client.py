import dagster as dg
import httpx


class WebClient(dg.ConfigurableResource):
    base_url: str

    @property
    def client(self) -> httpx.Client:
        return httpx.Client(base_url=self.base_url)


@dg.definitions
def resources():
    return dg.Definitions(resources={"noaa_client": WebClient(base_url="https://services.swpc.noaa.gov")})
