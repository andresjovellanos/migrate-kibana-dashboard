import json
import requests
import functions


def get_kibana_objects(es_endpoint, set_size, logger):
    url = "https://" + es_endpoint + "/.kibana/_search"
    query = {
        'query': {
            'terms': {
                'type': ['search', 'visualization', 'dashboard']
            }
        }
    }
    res = requests.get(url + "?size=" + str(set_size), json=query)
    if res.status_code in [200, 201]:
        return res.json()
    else:
        logger.error("Query failed: " + res.text)
        exit(1)


def get_dashboards_setting(es_endpoint, logger):
    jn = get_kibana_objects(es_endpoint, 0, logger)
    total = jn['hits']['total']
    res = get_kibana_objects(es_endpoint, total, logger)
    settings_set = res['hits']['hits']
    logger.debug("Queried " + str(len(settings_set)) + " dashboards settings from " + es_endpoint)
    return settings_set


def write_template(path, json_content):
    out = open(path, 'w+')
    json.dump(json_content, out)
    out.close()


def to_template_item(item, logger):
    type = item['_source']['type']
    id = item["_id"].replace(type + ":", '')
    logger.debug("Mapping item id[" + id + "]")
    source = dict(item['_source'][type])

    keys_blacklist = ['hits', 'timeRestore']
    for key in keys_blacklist:
        if key in source:
            del source[key]

    return {
        '_id': id,
        '_type': type,
        '_source': source
    }


def main():
    root_logger = functions.setup_logging()
    functions.check_vars(root_logger)
    region, profile, domain_name, template = functions.set_vars(root_logger)
    es_endpoint = functions.get_es_endpoint(domain_name, profile, root_logger, region="us-east-1")
    es_client = functions.get_es_client(es_endpoint)
    default_index = functions.get_kibana_default_index(es_client)
    root_logger.debug(msg=default_index)
    dashboard_settings = get_dashboards_setting(es_endpoint, root_logger)
    dashboard_items = json.loads(json.dumps(dashboard_settings).replace(default_index, "[[index]]"))
    template_data = [to_template_item(item, root_logger) for item in dashboard_items]
    write_template(template, template_data)
    root_logger.info(msg=f"{'-'*40}")
    root_logger.info(msg="Getting template: Done")
    root_logger.info(msg=f"{'-'*40}")
    exit(0)


if __name__ == '__main__':
    main()