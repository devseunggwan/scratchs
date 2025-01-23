export AIRFLOW_NAME="airflow"
export AIRFLOW_NAMESPACE="airflow-cluster"

helm repo add apache-airflow https://airflow.apache.org
helm repo update

## create the namespace
kubectl create ns "$AIRFLOW_NAMESPACE"

## install using helm 3
helm install \
  "$AIRFLOW_NAME" \
  apache-airflow/airflow \
  --namespace "$AIRFLOW_NAMESPACE" \
  --debug


helm upgrade \
  "$AIRFLOW_NAME" \
  apache-airflow/airflow \
  --namespace "$AIRFLOW_NAMESPACE" \
  --values ./override-values.yaml \
  --debug