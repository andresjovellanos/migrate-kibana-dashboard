# migrate-kibana-dashboard
Helps you migrating Kibana dashboards from one Elasticsearch to another 
one in AWS.

## Steps:

1) Create dashboards in Kibana
2) Generate a template from those dashboards
3) Push them to another ES instance

## How to run it:
You will need to set up these environment variables:
`ES_DOMAIN` (The AWS ES Domain used to retrieve the dashboards and 
visualizations)

**Docker compose**

- The idea here is to use `docker-compose up` to take the dashboards from
 `ES_DOMAIN` and push them to `ES_DOMAIN_TO_PROVISION`.
- If you use the Docker compose you will need this variable too:
 `ES_DOMAIN_TO_PROVISION` (this will be the Domain to provision)
- In case you are provision to a different account or region please modify
the variables accordingly.

**Docker** 

- Build your image: 
>  `docker build -t migrate-kibana .`
- Run the template retriever, here I'm mounting a volume so I'll keep the
template in the repo's directory.

>` docker run -ti --rm -e AWS_PROFILE -e ES_DOMAIN -v $HOME/.aws:/root/.aws -v $(PWD):/app migrate-kibana`
- Run the provisioner:

>`docker run -ti --rm -e AWS_PROFILE -e ES_DOMAIN=$ES_DOMAIN_TO_PROVISION -v $HOME/.aws:/root/.aws -v $(PWD):/app migrate-kibana python provisioner.py`

## Defaults
>REGION=us-east-1

>TEMPLATE_PATH="/app/template.json"




## Considerations:
- You should have the same index patterns and fields in both ES instances
- You can choose to keep the template in your repo so you have versioning,
otherwise you can develop a different mechanism.
- This tool wasn't tested with ES > 6.8
