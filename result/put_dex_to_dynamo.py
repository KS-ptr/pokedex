import boto3
from json import load, loads
import decimal
import configparser
from sys import argv

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    aws_config = config["AWS"]
    region_name = aws_config["region_name"]
    aws_access_key_id = aws_config["aws_access_key_id"]
    aws_secret_access_key = aws_config["aws_secret_access_key"]

    dynamo = boto3.resource('dynamodb', \
        endpoint_url='https://dynamodb.ap-northeast-1.amazonaws.com/:8000', \
        region_name=region_name, \
        aws_access_key_id=aws_access_key_id, \
        aws_secret_access_key=aws_secret_access_key)
    
    if argv[1] == "1":
        import_pokedex(dynamo)
    elif argv[1] == "2":
        import_else(dynamo, argv[2])

def import_pokedex(dynamodb):
    table = dynamodb.Table('pokedex')
    with open('./result/pokedex.json', encoding="utf-8") as f:
        items = load(f, parse_float=decimal.Decimal)
    
    items.sort(key=lambda x: x["number"])
    i = 0
    for item in items:
        item.pop("id")
        i += 1
        item["id"] = i
        response = table.put_item(
            Item=item
        )
    return response

def import_moves(dynamodb, file):
    if file == "pokedex":
        print("as argv[2], only 'moves', 'abilities', 'types', 'items' allowed.")
        return 0
    table = dynamodb.Table(file)
    with open('./result/{0}.json'.format(file), encoding="utf-8") as f:
        items = load(f)
    
    for item in items:
        response = table.put_item(Item=item)
    return response

if __name__ == '__main__':
    main()