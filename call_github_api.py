import requests,os,sys,json

fileName=sys.argv[1]
data=json.load(open(fileName))
searchWord=data['tableName']
token=os.environ['GITHUB_TOKEN']
url=f"https://api.github.com/search/code?q={searchWord}+user:Chandu-9100"
headers={'Content-Type':'application/vnd.github+json','Authorization':"Bearer {}".format(token)}
response=requests.get(url,headers=headers)
result=response.json()
# print(result)
repos_and_files={}
for dic in result["items"]:
    if dic['repository']['full_name'] not in repos_and_files:
        repos_and_files[dic['repository']['full_name']]=[]
        repos_and_files[dic['repository']['full_name']].append(dic['path'])
    else:
        repos_and_files[dic['repository']['full_name']].append(dic['path'])
print(repos_and_files)

