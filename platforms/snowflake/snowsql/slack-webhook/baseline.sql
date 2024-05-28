-- ref: https://medium.com/snowflake/send-slack-messages-from-snowflake-with-snowpark-external-network-access-8e3e42a7cde2

CREATE OR REPLACE NETWORK RULE slack_webhook_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('hooks.slack.com');

CREATE OR REPLACE SECRET slack_app_webhook_url
    type = GENERIC_STRING
    secret_string = ''
    comment = 'Slack Webhook URL you have created from the Slack App UI';

CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION slack_webhook_access_integration
  ALLOWED_NETWORK_RULES = (slack_webhook_network_rule)
  ALLOWED_AUTHENTICATION_SECRETS = (slack_app_webhook_url)
  ENABLED = true;


CREATE OR REPLACE PROCEDURE send_slack_message(MSG string)
    RETURNS STRING
    LANGUAGE PYTHON
    RUNTIME_VERSION = 3.10
    HANDLER = 'main'
    EXTERNAL_ACCESS_INTEGRATIONS = (slack_webhook_access_integration)
    SECRETS = ('slack_url' = slack_app_webhook_url)
    PACKAGES = ('snowflake-snowpark-python', 'requests')
    EXECUTE AS CALLER
AS
$$
import json
from datetime import date

import _snowflake
import snowflake.snowpark as snowpark
import requests

def main(session, msg): 
    # Retrieve the Webhook URL from the SECRET object
    webhook_url = _snowflake.get_generic_secret_string('slack_url')

    slack_data = {
     "text": f"Snowflake says: {msg}"
    }

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
    
    return "SUCCESS"
$$;


CALL send_slack_message('Hello world!');

CREATE OR REPLACE STAGE plot_stage ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

CREATE OR REPLACE PROCEDURE slack_snowflake_cost_report()
    RETURNS STRING
    LANGUAGE PYTHON
    RUNTIME_VERSION = 3.8
    HANDLER = 'main'
    EXTERNAL_ACCESS_INTEGRATIONS = (slack_webhook_access_integration)
    SECRETS = ('slack_url' = slack_app_webhook_url)
    PACKAGES = ('snowflake-snowpark-python', 'seaborn', 'matplotlib', 'requests', 'pandas')
    EXECUTE AS CALLER
AS
$$
import json
from datetime import date

import _snowflake
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col, dateadd, current_date, sum as sum_, lit


def generate_credit_spend_summary(session) -> pd.DataFrame:
    """
        Queries Snowflake ACCOUNT_USAGE views to generate a compute cost report 
        for the past 30 days.
    """
    
    dataframe = session.table('snowflake.account_usage.metering_daily_history').\
        filter(col("usage_date") >= dateadd('day', lit(-30), current_date())).\
        group_by(col("usage_date")).\
        agg(sum_("credits_billed").alias("credits_billed")).\
        sort(col("usage_date"), ascending=False)

    dataframe_pd = dataframe.to_pandas()

    return dataframe_pd

    
def generate_plot(session, df: pd.DataFrame) -> str:
    """
        Generates plot, saves it to a Snowflake Stage, and outputs the Presigned URL
    """
    
    # Set the figure size
    plt.figure(figsize=(8, 4))

    sns.barplot(x='USAGE_DATE', y='CREDITS_BILLED', color='blue', data=df)

    # Rotate x-axis labels for better visibility (optional)
    plt.xticks(rotation=45)

    # Set labels and title
    plt.xlabel('Date')
    plt.ylabel('Credits')
    plt.title('Credit spend - Last 30 days')

    plt.tight_layout()
    plt.savefig('/tmp/credit_spend_l30days.png')

    session.file.put('/tmp/credit_spend_l30days.png', '@PLOT_STAGE', overwrite=True, auto_compress=False)

    # Generate a Presigned URL with a TTL of 15s
    df = session.sql("SELECT GET_PRESIGNED_URL(@PLOT_STAGE, 'credit_spend_l30days.png', 15) as image_url").collect()
    
    return df[0][0]

    
def main(session):
    """
        Main SPROC handler.
    """

    # Retrieve Slack Webhook URL from the SECRET object
    webhook_url = _snowflake.get_generic_secret_string('slack_url')
    
    credit_spend_summary_df = generate_credit_spend_summary(session)
    image_url = generate_plot(session, credit_spend_summary_df)

    slack_data = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"Snowflake credit spend report for {date.today()}",
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Total credits spent in the past 30 days: *{credit_spend_summary_df['CREDITS_BILLED'].sum()}*"
                }
            },
            {
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": "Daily Snowflake credit spend"
                },
                "block_id": "image4",
                "image_url": image_url,
                "alt_text": "Snowflake credit spend report"
            }
        ]
    }

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, Response:\n%s'
            % (response.status_code, response.text)
        )
    
    return "SUCCESS"
$$;

CALL slack_snowflake_cost_report();



