import google.auth
import google.auth.transport.requests
from google.oauth2 import service_account
import requests,sys,json,os

try:
    credential_json=json.loads(os.environ['credential_file'])
    data=json.load(open(sys.argv[1]))

    credentials = service_account.Credentials.from_service_account_info(credential_json,scopes=['https://www.googleapis.com/auth/cloud-platform'])

    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
    token=credentials.token
    final_data={}
    project_id=data["tableProjectId"]
    location=data["tableLocation"]
    dataset=data["tableDataset"]
    table=data["tableName"]
    final_data[table]=[]
    parent=f"projects/{project_id}/locations/{location}"
    body={"source":{"fullyQualifiedName":f"bigquery:{project_id}.{dataset}.{table}"}}
    headers={'Content-Type':'application/json','Authorization':"Bearer {}".format(token)}
    response=requests.post(f'https://datalineage.googleapis.com/v1/{parent}:searchLinks',headers=headers,json=body)
    result=response.json()['links']
    # print(result)
    for val in result:
        target_table=val['target']['fullyQualifiedName'].split(':')[-1]
        final_data[table].append(target_table)
    print(final_data)
except Exception as e:
    print(e)
