from pyspark.sql.functions import *
from pyspark.sql.types import *
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Event Hubs configuration
EH_NAMESPACE = "ubereventsprojec"
EH_NAME = "ubertopic"

# Get connection string securely
EH_CONN_STR = os.getenv("EH_CONN_STR")

KAFKA_OPTIONS = {
    "kafka.bootstrap.servers": f"{EH_NAMESPACE}.servicebus.windows.net:9093",
    "subscribe": EH_NAME,
    "kafka.sasl.mechanism": "PLAIN",
    "kafka.security.protocol": "SASL_SSL",
    "kafka.sasl.jaas.config":
        f'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="{EH_CONN_STR}";',
    "kafka.request.timeout.ms": 10000,
    "kafka.session.timeout.ms": 10000,
    "maxOffsetsPerTrigger": 10000,
    "failOnDataLoss": "true",
    "startingOffsets": "earliest"
}

df = spark.readStream.format("kafka") \
    .options(**KAFKA_OPTIONS) \
    .load()

df = df.withColumn("rides", col("value").cast(StringType()))

display(
    df,
    checkpointLocation="/Volumes/uber/bronze/my_volume/volume_folder/"
)