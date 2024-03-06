from datetime import datetime
import random
import os  # Import the os module to work with environment variables
from dotenv import load_dotenv  # Import load_dotenv function from dotenv module
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_resource import MetricResource
from datadog_api_client.v2.model.metric_series import MetricSeries

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and application key from environment variables
api_key = os.getenv("DD_API_KEY")
app_key = os.getenv("DD_APPLICATION_KEY")

print("API Key:", api_key)
print("Application Key:", app_key)

configuration = Configuration(
    host="https://us5.datadoghq.com"
)
configuration.api_key['apiKeyAuth'] = api_key
configuration.api_key['appKeyAuth'] = app_key

while True:
    random_value = random.random()

    body = MetricPayload(
        series=[
            MetricSeries(
                metric="potato_metric", 
                type=MetricIntakeType.UNSPECIFIED,
                points=[
                    MetricPoint(
                        timestamp=int(datetime.now().timestamp()),
                        value=random_value,
                    ),
                ],
                resources=[
                    MetricResource(
                        name="localhost",
                        type="host",
                    ),
                ],
                tags=["method:test","custom:metrics"]
            ),
        ],
    )

    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        response = api_instance.submit_metrics(body=body)

        print(response)
        print(configuration.api_key)
