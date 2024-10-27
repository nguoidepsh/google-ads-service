import asyncio
from uuid import UUID

import proto
from controllers.email_controller import get_email_by_mail
from db.db_connector import DB_SESSION
from settings import TRACKING_URL_TEMPLATE
from fastapi import HTTPException, Request, status
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from settings import get_credentials
from google.api_core import protobuf_helpers


async def list_accounts(session: DB_SESSION, email: str):
    """
    Get a list of Google Ads accounts using the provided email.
    """
    email = get_email_by_mail(session, email=email)

    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found",
        )

    credentials = get_credentials(refresh_token=email.refresh_token)
    client = GoogleAdsClient.load_from_dict(credentials)
    customer_service = client.get_service("CustomerService")
    accessible_customers = customer_service.list_accessible_customers()

    accounts = []
    for account_resource_name in accessible_customers.resource_names:
        customer_id = account_resource_name.split("/")[-1]
        response = await list_child_accounts(client, customer_id)
        accounts += response

    return accounts

async def list_child_accounts(client, customer_id: str = None):
    """
    Get a list of child accounts under the given MCC account.
    """
    google_ads_service = client.get_service("GoogleAdsService")
    query = """
        SELECT
            customer_client.client_customer,
            customer_client.level,
            customer_client.manager,
            customer_client.descriptive_name,
            customer_client.currency_code,
            customer_client.time_zone,
            customer_client.id,
            customer_client.status
        FROM
            customer_client
        WHERE
            customer_client.status <> 'CANCELED'
    """
    try:
        response = await asyncio.to_thread(
            google_ads_service.search, customer_id=customer_id, query=query
        )
    except GoogleAdsException:
        return []

    account_details = []
    for row in response:
        customer_client = row.customer_client
        details = {
            "id": customer_client.id,
            "descriptive_name": customer_client.descriptive_name,
            "currency_code": customer_client.currency_code,
            "time_zone": customer_client.time_zone,
            "level": customer_client.level,
            "manager": customer_client.manager,
            "status": customer_client.status.name,
            "login_customer_id": customer_id,
        }
        account_details.append(details)

    return account_details

async def list_campaigns(
    session: DB_SESSION, email: str, customer_id: str, login_customer_id: str
):
    """
    Get a list of campaigns for the given customer ID.
    """
    email = get_email_by_mail(session, email=email)

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    credentials = get_credentials(
        refresh_token=email.refresh_token, login_customer_id=login_customer_id
    )
    client = GoogleAdsClient.load_from_dict(credentials)
    google_ads_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.start_date,
            campaign.end_date,
            campaign.tracking_url_template
        FROM
            campaign
    """
    response = await asyncio.to_thread(
        google_ads_service.search, customer_id=customer_id, query=query
    )

    campaign_details = []
    for row in response:
        campaign = row.campaign
        campaign_details.append(
            {
                "resource_name": campaign.resource_name,
                "id": campaign.id,
                "name": campaign.name,
                "status": campaign.status.name,
                "start_date": campaign.start_date,
                "end_date": campaign.end_date,
                "tracking_url_template": campaign.tracking_url_template,
            }
        )

    return campaign_details

async def get_data(
    session: DB_SESSION,
    email: str,
    customer_id: str,
    campaign_id: str,
    login_customer_id: str,
):
    """
    Get data for a specific campaign.
    """
    email = get_email_by_mail(session, email=email)
    credentials = get_credentials(
        refresh_token=email.refresh_token, login_customer_id=login_customer_id
    )
    client = GoogleAdsClient.load_from_dict(credentials)
    google_ads_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            landing_page_view.resource_name,
            metrics.clicks,
            metrics.cost_micros,
            metrics.average_cpc,
            metrics.impressions,
            ad_group.id,
            segments.device,
            segments.date,
            campaign.id
        FROM
            landing_page_view
        WHERE segments.date BETWEEN '2000-01-01' AND '2100-01-01'
        AND campaign.id = {campaign_id}
    """
    response = await asyncio.to_thread(
        google_ads_service.search, customer_id=customer_id, query=query
    )

    return [proto.Message.to_dict(row) for row in response]

async def set_tracking(
    session: DB_SESSION, email: str, campaign_id: str, project_id: str, customer_id: str, login_customer_id: str
):
    print(email, campaign_id, login_customer_id)
    """
    Set tracking URL template for a specific campaign.
    """
    email = get_email_by_mail(session, email=email)
    credentials = get_credentials(
        refresh_token=email.refresh_token, login_customer_id=login_customer_id
    )
    client = GoogleAdsClient.load_from_dict(credentials)

    campaign_service = client.get_service("CampaignService")
    # Create campaign operation.
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.update

    campaign.resource_name = campaign_service.campaign_path(
        customer_id, campaign_id
    )

    campaign.tracking_url_template = TRACKING_URL_TEMPLATE.replace("UUID", str(email.uuid)).replace("PROJECT_ID", str(project_id))
    client.copy_from(
        campaign_operation.update_mask,
        protobuf_helpers.field_mask(None, campaign._pb),
    )


    response = await asyncio.to_thread(
        campaign_service.mutate_campaigns, customer_id=customer_id, operations=[campaign_operation]
    )

    return proto.Message.to_dict(response.results[0].campaign)
