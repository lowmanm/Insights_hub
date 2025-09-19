"""
API views for the analytics app.

This module defines a few simple endpoints as a starting point.  The
production implementation should authenticate callers, parse user
queries, run parameterised SQL against BigQuery and interface with a
large‑language model to generate natural‑language answers.  For now,
these views return stubbed responses to illustrate the shape of the
responses you might send to the frontend.
"""

import logging
from typing import Any, Dict

from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .auth import SaviyntAuthentication
from . import ai

try:
    from google.cloud import bigquery  # type: ignore
except ImportError:
    bigquery = None  # will be None in test environments without the package

logger = logging.getLogger(__name__)


def _get_bigquery_client() -> "bigquery.Client | None":
    """Return a BigQuery client initialised from environment variables.

    If the google.cloud.bigquery library is not installed, return None.
    """
    if bigquery is None:
        logger.warning("google.cloud.bigquery is not installed; returning None")
        return None
    # The client will automatically use credentials specified via the
    # GOOGLE_APPLICATION_CREDENTIALS environment variable or default
    # application credentials.
    try:
        client = bigquery.Client(project=settings.GCP_PROJECT_ID)
        return client
    except Exception as e:  # pragma: no cover
        logger.exception("Failed to create BigQuery client: %s", e)
        return None


@api_view(['GET'])
def ping(request):
    """Health check endpoint to verify the API is reachable."""
    return Response({'status': 'ok'})


@api_view(['GET'])
def insights_summary(request):
    """Return a summary of key metrics for the Insights Hub.

    In a production implementation this function would build and execute
    parameterised SQL queries against BigQuery to compute prior day,
    month‑to‑date and predicted metrics.  To keep this skeleton simple we
    return hard‑coded numbers.  Replace these stubs with real queries
    using the `google.cloud.bigquery` client.
    """
    # Example stub data; replace with results of BigQuery queries
    summary: Dict[str, Any] = {
        'prior_day_total_orders': 1234,
        'prior_day_on_time_rate': 0.93,
        'mtd_total_orders': 28976,
        'mtd_on_time_rate': 0.91,
        'prediction_today_total_orders': 1340,
        'prediction_today_on_time_rate': 0.94,
    }
    return Response(summary)


@api_view(['POST'])
@authentication_classes([SaviyntAuthentication])
@permission_classes([])  # Permissions can be refined later
def chat(request):
    """A simple chat endpoint that echoes the user's query.

    This endpoint is intended to act as the backend for a chat bot.  In
    a full implementation you would parse the question, decide which
    tables and fields are relevant, construct a SQL query against
    BigQuery, execute it, and then compose a natural language response.
    Here we simply echo the input to demonstrate the API contract.
    """
    data = request.data
    if not isinstance(data, dict) or 'query' not in data:
        return Response({'error': 'Missing "query" in request body'}, status=status.HTTP_400_BAD_REQUEST)
    user_query: str = str(data['query'])
    # Call Vertex AI via the helper.  The helper will return a stubbed
    # response if the aiplatform library is not installed or the model
    # name is not configured.
    bot_answer = ai.call_vertex_ai(user_query)
    return Response({'response': bot_answer})
