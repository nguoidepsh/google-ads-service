import asyncio
import datetime
from uuid import UUID

import proto
from controllers.account_controller import valid_owner
from controllers.email_controller import get_email_by_mail
from db.db_connector import DB_SESSION
from fastapi import Depends, HTTPException, Request, status
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.api_core import protobuf_helpers
from models.account_model import Account
from settings import TRACKING_URL_TEMPLATE, get_credentials


async def get_credentials_by_email(
    session: DB_SESSION, email: str, login_customer_id: str = None
):
    """
    Get credentials using the provided email.
    """
    email = get_email_by_mail(session, email=email)

    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found",
        )

    credentials = get_credentials(
        refresh_token=email.refresh_token, login_customer_id=login_customer_id
    )
    return GoogleAdsClient.load_from_dict(credentials)


async def list_accounts(client: GoogleAdsClient = Depends(get_credentials_by_email)):
    """
    Get a list of Google Ads accounts using the provided email.
    """
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
            customer_client.status <> 'CANCELED' AND customer_client.status <> 'SUSPENDED'
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
    customer_id: str,
    client: GoogleAdsClient = Depends(get_credentials_by_email),
):
    """
    Get a list of campaigns for the given customer ID.
    """

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
    customer_id: str,
    campaign_id: str,
    client: GoogleAdsClient = Depends(get_credentials_by_email),
):
    """
    Get data for a specific campaign.
    """
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
    campaign_id: str,
    project_id: str,
    customer_id: str,
    client: GoogleAdsClient = Depends(get_credentials_by_email),
):
    """
    Set tracking URL template for a specific campaign.
    """

    campaign_service = client.get_service("CampaignService")
    # Create campaign operation.
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.update

    campaign.resource_name = campaign_service.campaign_path(customer_id, campaign_id)

    campaign.tracking_url_template = TRACKING_URL_TEMPLATE.replace(
        "UUID", str(email.uuid)
    ).replace("PROJECT_ID", str(project_id))
    client.copy_from(
        campaign_operation.update_mask,
        protobuf_helpers.field_mask(None, campaign._pb),
    )

    response = await asyncio.to_thread(
        campaign_service.mutate_campaigns,
        customer_id=customer_id,
        operations=[campaign_operation],
    )

    return proto.Message.to_dict(response.results[0].campaign)


def create_billing_setup(
    client, customer_id, payments_account_id=None, payments_profile_id=None
):
    """Creates and returns a new billing setup instance.

    The new billing setup will have its payment details populated. One of the
    payments_account_id or payments_profile_id must be provided.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        payments_account_id: payments account ID to attach to the new billing
            setup. If provided it must be formatted as "1234-5678-9012-3456".
        payments_profile_id: payments profile ID to attach to a new payments
            account and to the new billing setup. If provided it must be
            formatted as "1234-5678-9012".

    Returns:
        A newly created BillingSetup instance.
    """
    billing_setup = client.get_type("BillingSetup")

    # Sets the appropriate payments account field.
    if payments_account_id != None:
        # If a payments account ID has been provided, set the payments_account
        # field to the full resource name of the given payments account ID.
        # You can list available payments accounts via the
        # PaymentsAccountService's ListPaymentsAccounts method.
        billing_setup.payments_account = client.get_service(
            "BillingSetupService"
        ).payments_account_path(customer_id, payments_account_id)
    elif payments_profile_id != None:
        # Otherwise, create a new payments account by setting the
        # payments_account_info field
        # See https://support.google.com/google-ads/answer/7268503
        # for more information about payments profiles.
        billing_setup.payments_account_info.payments_account_name = (
            f"Payments Account #{uuid4()}"
        )
        billing_setup.payments_account_info.payments_profile_id = payments_profile_id

    return billing_setup


def set_billing_setup_date_times(client, customer_id, billing_setup):
    """Sets the starting and ending date times for the new billing setup.

    Queries the customer's account to see if there are any approved billing
    setups. If there are any, the new billing setup starting date time is set to
    one day after the last. If not, the billing setup is set to start
    immediately. The ending date is set to one day after the starting date time.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        billing_setup: the billing setup whose starting and ending date times
            will be set.
    """
    # The query to search existing approved billing setups in the end date time
    # descending order. See get_billing_setup.py for a more detailed example of
    # how to retrieve billing setups.
    query = """
      SELECT
        billing_setup.end_date_time
      FROM billing_setup
      WHERE billing_setup.status = APPROVED
      ORDER BY billing_setup.end_date_time DESC
      LIMIT 1"""

    ga_service = client.get_service("GoogleAdsService")
    stream = ga_service.search_stream(customer_id=customer_id, query=query)
    # Coercing the response iterator to a list causes the stream to be fully
    # consumed so that we can easily access the last row in the request.
    batches = list(stream)
    # Checks if any results were included in the response.
    if batches:
        # Retrieves the ending_date_time of the last BillingSetup.
        last_batch = batches[0]
        last_row = last_batch.results[0]
        last_ending_date_time = last_row.billing_setup.end_date_time

        if not last_ending_date_time:
            # A null ending date time indicates that the current billing setup
            # is set to run indefinitely. Billing setups cannot overlap, so
            # throw an exception in this case.
            raise Exception(
                "Cannot set starting and ending date times for the new billing "
                "setup; the latest existing billing setup is set to run "
                "indefinitely."
            )

        try:
            # BillingSetup.end_date_time is a string that can be in the format
            # %Y-%m-%d or %Y-%m-%d %H:%M:%S. This checks for the first format.
            end_date_time_obj = datetime.strptime(last_ending_date_time, "%Y-%m-%d")
        except ValueError:
            # If a ValueError is raised then the end_date_time string is in the
            # second format that includes hours, minutes and seconds.
            end_date_time_obj = datetime.strptime(
                last_ending_date_time, "%Y-%m-%d %H:%M:%S"
            )

        # Sets the new billing setup start date to one day after the end date.
        start_date = end_date_time_obj + timedelta(days=1)
    else:
        # If there are no BillingSetup objects to retrieve, the only acceptable
        # start date time is today.
        start_date = datetime.now()

    billing_setup.start_date_time = start_date.strftime("%Y-%m-%d %H:%M:%S")
    billing_setup.end_date_time = (start_date + timedelta(days=1)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


async def new_billing(client, customer_id, login_customer_id):
    """Thêm phương thức thanh toán cho tài khoản."""
    billing_setup_service = client.get_service("BillingSetupService")
    billing_setup_operation = client.get_type("BillingSetupOperation")
    billing_setup = billing_setup_operation.create
    billing_setup.payments_account = billing_setup_service.payments_account_path(
        customer_id, "3204-8699-9879-9708"
    )
    billing_setup.start_date_time = "2024-12-24"

    # client.copy_from(billing_setup_operation.create, billing_setup)
    response = billing_setup_service.mutate_billing_setup(
        customer_id=customer_id, operation=billing_setup_operation
    )
    return response


async def get_account_budget(client, account: Account):
    """Lấy thông tin Account Budget hiện tại."""
    ga_service = client.get_service("GoogleAdsService")
    query = """
        SELECT account_budget.resource_name,
               account_budget.proposed_spending_limit_micros,
               account_budget.status
        FROM account_budget
        WHERE account_budget.status = 'APPROVED'
    """
    response = ga_service.search(customer_id=account.customer_id, query=query)
    for row in response:
        return row.account_budget
    return None


async def update_budget(client, customer_id, account_budget, amount):
    """Cập nhật ngân sách tài khoản Google Ads bằng cách tạo một proposal mới."""
    proposal_service = client.get_service("AccountBudgetProposalService")

    # Tạo AccountBudgetProposalOperation
    account_budget_proposal_operation = client.get_type(
        "AccountBudgetProposalOperation"
    )
    proposal = account_budget_proposal_operation.create

    # Cấu hình proposal
    proposal.proposal_type = client.enums.AccountBudgetProposalTypeEnum.UPDATE
    proposal.account_budget = account_budget.resource_name
    proposal.proposed_spending_limit_micros = (
        account_budget.proposed_spending_limit_micros + amount * 1_000_000
    )

    # Tạo field mask (nếu cần)
    field_mask = protobuf_helpers.field_mask(None, proposal._pb)
    # field_mask = field_mask_pb2.FieldMask(paths=["proposed_spending_limit_micros"])
    account_budget_proposal_operation.update_mask.CopyFrom(field_mask)

    # Gửi yêu cầu
    try:
        response = proposal_service.mutate_account_budget_proposal(
            customer_id=customer_id, operation=account_budget_proposal_operation
        )
        print(f"Proposal updated: {response.result.resource_name}")
        return response.result.resource_name
    except Exception as e:
        print(f"Error updating account budget proposal: {e}")
        return None


def main(client, customer_id, payments_account_id=None, payments_profile_id=None):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        payments_account_id: payments account ID to attach to the new billing
            setup. If provided it must be formatted as "1234-5678-9012-3456".
        payments_profile_id: payments profile ID to attach to a new payments
            account and to the new billing setup. If provided it must be
            formatted as "1234-5678-9012".
    """
    billing_setup = create_billing_setup(
        client, customer_id, payments_account_id, payments_profile_id
    )
    set_billing_setup_date_times(client, customer_id, billing_setup)
    billing_setup_operation = client.get_type("BillingSetupOperation")
    client.copy_from(billing_setup_operation.create, billing_setup)
    billing_setup_service = client.get_service("BillingSetupService")
    response = billing_setup_service.mutate_billing_setup(
        customer_id=customer_id, operation=billing_setup_operation
    )
    print(
        "Added new billing setup with resource name " f"{response.result.resource_name}"
    )


async def deposit(
    session: DB_SESSION, amount: int, account: Account = Depends(valid_owner)
):
    """
    Add payment method to the account.
    """
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not available.",
        )
    client = await get_credentials_by_email(
        session, account.email, account.login_customer_id
    )

    account_budget = await get_account_budget(client, account)
    if not account_budget:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Account budget not found."
        )

    response = await update_budget(client, account.customer_id, account_budget, amount)
    # main(
    #     googleads_client,
    #     args.customer_id,
    #     args.payments_account_id,
    #     args.payments_profile_id,
    # )
    # resp = await new_billing(client, account.customer_id, account.login_customer_id)

    # print(resp.resource_name)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Budget update failed.",
        )
    return {"account": account, "amount": amount}
