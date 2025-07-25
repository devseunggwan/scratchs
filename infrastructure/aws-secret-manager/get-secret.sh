SECRET_ID=""

aws secretsmanager get-secret-value --secret-id $SECRET_ID --query SecretString --output text
