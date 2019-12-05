import boto3
from elasticsearch import Elasticsearch
import certifi
import logging
import os

def set_vars(logger):
    logger.info("Setting env vars")
    region = os.environ["AWS_REGION"]
    profile = os.environ["AWS_PROFILE"]
    domain_name = os.environ["ES_DOMAIN"]
    template = os.getenv("TEMPLATE_PATH", "/app/template.json")
    return region, profile, domain_name, template

def check_vars(logger):
    needed_vars = ["AWS_PROFILE", "ES_DOMAIN"]
    logger.info("checking ENV variables")
    logger.debug(os.environ)
    for var in needed_vars:
        if var not in os.environ:
            logger.error(f"Missing variable: {var}")
            exit(1)


def setup_logging():
    format = '%(asctime)s [%(levelname)s]  %(message)s'
    logging.basicConfig(format=format, level=logging.INFO)
    root_log = logging.getLogger()
    return root_log


def get_es_endpoint(domain_name, profile, logger, region):
    session = boto3.Session(profile_name=profile)
    es = session.client('es', region)
    domain_description = es.describe_elasticsearch_domain(DomainName=domain_name)
    endpoint = domain_description['DomainStatus']['Endpoint']
    logger.debug(msg="Endpoint: " + endpoint)
    return endpoint


def get_es_client(endpoint):
    return Elasticsearch(
        [endpoint],
        scheme="https",
        port=443,
        use_ssl=True,
        verify_certs=True,
        ca_certs=certifi.where(),
    )


def get_kibana_default_index(es_client):
    default_index_response = es_client.search(index=".kibana", body={
        "_source": ["config.defaultIndex"],
        "query": {
            "match": {
                "type": "config"
            }
        }
    })
    return default_index_response['hits']['hits'][0]['_source']['config']['defaultIndex']


def get_template(template_file_path):
    file_object = open(template_file_path, 'r')
    content = file_object.read()
    file_object.close()
    return content
