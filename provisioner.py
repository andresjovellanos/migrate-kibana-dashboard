import json
import functions
import requests

def execute_update_request(id, type, data, es_endpoint, logger):
    url = "https://" + es_endpoint + "/.kibana/doc/" + type + ":" + id
    logger.debug("Url = " + url)
    logger.debug("Data = ")
    logger.debug(data)
    res = requests.put(url, json=data)
    logger.debug("Status code: %s " % res.status_code )
    if res.status_code in [200, 201]:
        return res.json()
    else:
        logger.error("Query failed: " + res.text)
        exit(1)


def update_items_kibana_index(item, es_endpoint, logger):
    id = item["_id"]
    type = item["_type"]
    source = item["_source"]
    data = json.loads('{}')
    data['type'] = type
    data[type] = source
    execute_update_request(id, type, data, es_endpoint, logger)
    logger.info(f"Updating item id: {id}, of type: {type}")


def main():
    root_logger = functions.setup_logging()
    functions.check_vars(root_logger)
    region, profile, domain_name, template = functions.set_vars(root_logger)
    es_endpoint = functions.get_es_endpoint(domain_name, profile, root_logger, region='us-east-1')
    es_client = functions.get_es_client(es_endpoint)
    default_index = functions.get_kibana_default_index(es_client)
    root_logger.info(msg=default_index)
    replaced = functions.get_template(template).replace("[[index]]", default_index)
    import_data = json.loads(replaced)
    [update_items_kibana_index(item, es_endpoint, root_logger) for item in import_data]
    root_logger.info(msg=f"{'-'*40}")
    root_logger.info(msg="Provisioning Done")
    root_logger.info(msg=f"{'-'*40}")
    exit(0)


if __name__ == '__main__':
    main()
