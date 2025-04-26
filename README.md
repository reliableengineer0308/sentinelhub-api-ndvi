# 🌍 NDVI Calculation API using FastAPI & SentinelHub

This project provides a simple FastAPI-based API endpoint to calculate `NDVI` (Normalized Difference Vegetation Index) statistics over a given polygon using SentinelHub services.

## 📦 Features

- Accepts GeoJSON input to define an area of interest.
- Queries Sentinel-2 L2A data through SentinelHub.
- Calculates daily NDVI values for the given period (`2022-01-01` to `2022-11-30`).
- Returns histogram-based NDVI statistics.

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://your-repo-url.git
cd your-repo-folder
```

### 2. Install the dependencies
```bash
pip install fastapi uvicorn pydantic shapely sentinelhub
```

### 3. Set SentinelHub Credentials
Make sure you set the correct SentinelHub credentials:
```bash
config.instance_id = 'YOUR_INSTANCE_ID'
config.sh_client_id = 'YOUR_CLIENT_ID'
config.sh_client_secret = 'YOUR_CLIENT_SECRET'

```

Alternatively, you can configure them through environment variables or `sentinelhub.config` file.

### 4. Run the server
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.


## 📬 API Usage
Endpoint
`POST /ndvi`

### Request Body Example
```bash
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [13.822174072265625, 45.85080395917834],
            [14.5599365234375, 45.85080395917834],
            [14.5599365234375, 46.29191774991382],
            [13.822174072265625, 46.29191774991382],
            [13.822174072265625, 45.85080395917834]
          ]
        ]
      }
    }
  ]
}
```

### Response Example

Returns a JSON containing NDVI histogram statistics for the given area over the specified time interval.


## 📚 Technologies Used
1. FastAPI – API Framework
2. SentinelHub-py – SDK to interact with SentinelHub APIs
3. Pydantic – Data validation
4. Shapely – GeoJSON geometry parsing

## 🔥 Notes
- Be aware that the SentinelHub Service Worker can rate limit you based on your subscription plan.
- The NDVI calculation uses the formula:
```bash
NDVI = (NIR - RED) / (NIR + RED)
```