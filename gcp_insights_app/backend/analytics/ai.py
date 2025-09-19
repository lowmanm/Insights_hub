"""
Helpers for interacting with Vertex AI and BigQuery ML.

This module encapsulates calls to Google Vertex AI and BigQuery ML
models.  In this scaffold the functions are stubs that log their
inputs and return dummy outputs.  Replace them with actual calls to
`google.cloud.aiplatform` and parameterised SQL using the BigQuery
client once you have defined your machine learning models and
endpoints.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

try:
    from google.cloud import aiplatform  # type: ignore
except ImportError:
    aiplatform = None  # aiplatform is optional in test environments

from django.conf import settings

logger = logging.getLogger(__name__)


def call_vertex_ai(prompt: str) -> str:
    """Send a prompt to a Vertex AI generative model and return the response.

    When the `google.cloud.aiplatform` library is available and a model
    endpoint is configured via environment variables, this function will
    call the model and return its output.  Otherwise it returns a
    static string for demonstration purposes.
    """
    if aiplatform is None:
        logger.warning("google-cloud-aiplatform is not installed; returning stub response")
        return f"[Vertex AI stub] Echoing prompt: {prompt}"

    model_name = settings.VERTEX_MODEL_NAME if hasattr(settings, 'VERTEX_MODEL_NAME') else None
    if not model_name:
        logger.warning("VERTEX_MODEL_NAME environment variable is not set; returning stub response")
        return f"[Vertex AI stub] Echoing prompt: {prompt}"

    try:
        # Initialise Vertex AI client
        aiplatform.init(project=settings.GCP_PROJECT_ID, location=settings.VERTEX_LOCATION)
        model = aiplatform.TextGenerationModel.from_pretrained(model_name)
        response = model.predict(prompt)
        return response.text  # type: ignore[no-any-return]
    except Exception as exc:  # pragma: no cover
        logger.exception("Error calling Vertex AI: %s", exc)
        return f"[Vertex AI error] {exc}"


def run_bigquery_ml_prediction(model_table: str, input_params: Dict[str, Any]) -> Dict[str, Any]:
    """Run a BigQuery ML model and return predictions.

    Given the fully qualified table name of a BigQuery ML model and a set
    of input parameters, construct and execute a SQL query to obtain
    predictions.  In this scaffold the function returns a static
    prediction.  Replace this stub with a call to the BigQuery client.
    """
    logger.info("Running BigQuery ML prediction on model %s with params %s", model_table, input_params)
    # TODO: Use google.cloud.bigquery to execute ML.PREDICT
    return {
        'prediction': 0.95,
        'model_table': model_table,
        'input': input_params,
    }
