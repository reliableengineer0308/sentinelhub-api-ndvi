from fastapi import FastAPI
from pydantic import BaseModel
from shapely.geometry import shape

from sentinelhub import (
    CRS,
    DataCollection,
    Geometry,
    SentinelHubStatistical,
    SentinelHubStatisticalDownloadClient,
    SHConfig
)

config = SHConfig()

config.instance_id = 'd508e70a-1569-406f-b91f-e7cbd3668b8d'
config.sh_client_id = '094f19f9-6fa1-4a66-88ec-73ba46903747'
config.sh_client_secret = '~w3e_tY}(UYnb7,uBy!_ufF7)fVgQ}z1gSEQElno'

app = FastAPI()


class Feature(BaseModel):
    type: str
    properties: dict
    geometry: dict = {
        'coordinates': []
    }


class Geo(BaseModel):
    type: str
    features: list[Feature]


@app.post("/ndvi")
async def ndvi(geo: Geo):
    Polygon = shape(geo.features[0].geometry)

    yearly_time_interval = "2022-01-01", "2022-11-30"

    ndvi_evalscript = """
    //VERSION=3

    function setup() {
    return {
        input: [
        {
            bands: [
            "B04",
            "B08",
            "dataMask"
            ]
        }
        ],
        output: [
        {
            id: "ndvi",
            bands: 1
        },
        {
            id: "dataMask",
            bands: 1
        }
        ]
    }
    }

    function evaluatePixel(samples) {
        return {
        ndvi: [index(samples.B08, samples.B04)],
        dataMask: [samples.dataMask]
        };
    }
    """

    aggregation = SentinelHubStatistical.aggregation(
        evalscript=ndvi_evalscript, time_interval=yearly_time_interval, aggregation_interval="P1D", resolution=(10, 10)
    )

    input_data = SentinelHubStatistical.input_data(
        DataCollection.SENTINEL2_L2A)

    histogram_calculations = {"ndvi": {"histograms": {
        "default": {"nBins": 20, "lowEdge": -1.0, "highEdge": 1.0}}}}

    ndvi_requests = []

    request = SentinelHubStatistical(
        aggregation=aggregation,
        input_data=[input_data],
        geometry=Geometry(Polygon, crs=CRS.WGS84),
        calculations=histogram_calculations,
        config=config,
    )
    ndvi_requests.append(request)

    download_requests = [ndvi_request.download_list[0]
                         for ndvi_request in ndvi_requests]

    client = SentinelHubStatisticalDownloadClient(config=config)

    ndvi_stats = client.download(download_requests)

    return ndvi_stats
