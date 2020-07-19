import boto3
from json import load, loads
import decimal
import configparser
from sys import argv

def main():
    if argv[1] == "1":
        import_pokedex()

def import_pokedex():
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

    table = dynamo.Table('pokedex')
    with open('./result/pokedex.json', encoding="utf-8") as f:
        items = load(f, parse_float=decimal.Decimal)
    
    items.sort(key=lambda x: x["number"])
    i = 0
    for item in items:
        item.pop("id")
        i += 1
        item["int_id"] = i
        response = table.put_item(
            Item=item
        )
    return response

if __name__ == '__main__':
    main()