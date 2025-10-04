from tqdm import tqdm
from pathlib import Path
import base64
from weaviate.util import generate_uuid5
import weaviate
from weaviate.classes.config import Configure, Property, DataType
from dotenv import load_dotenv
import os
import numpy as np
import json
from tools import COLLECTION_NAME

load_dotenv(override=True)

with weaviate.connect_to_weaviate_cloud(
    cluster_url=os.getenv("WEAVIATE_URL"),
    auth_credentials=os.getenv("WEAVIATE_ADMIN_KEY"),
    headers={
        "X-Cohere-Api-Key": os.getenv("COHERE_API_KEY"),
    }
) as client:
    client.collections.delete(COLLECTION_NAME)
    client.collections.create(
        name=COLLECTION_NAME,
        properties=[
            Property(
                name="model_name",
                data_type=DataType.TEXT,
            ),
            Property(
                name="page_image",
                data_type=DataType.BLOB,
            ),
            Property(
                name="filename",
                data_type=DataType.TEXT,
            ),
        ],
        vector_config=[
            Configure.Vectors.self_provided(name="default")
        ]
    )

    pages = client.collections.use(COLLECTION_NAME)

    with open("data/embeddings/embeddings_metadata.json", "r") as f:
        metadata = json.load(f)

    embeddings = np.load("data/embeddings/image_embeddings.npy")

    with pages.batch.fixed_size(batch_size=10) as batch:
        for i, embedding in tqdm(enumerate(embeddings)):
            filepath = Path(metadata["image_paths"][i])
            image = filepath.read_bytes()
            base64_image = base64.b64encode(image).decode('utf-8')
            obj = {
                "model_name": filepath.stem.split("_")[0],
                "page_image": base64_image,
                "filename": filepath.name
            }

            # Add object to batch for import with (batch.add_object())
            # This time, manually provide the vector with `{"default": embedding}`
            batch.add_object(
                properties=obj,
                uuid=generate_uuid5(str(filepath)),
                vector={"default": embedding}
            )
