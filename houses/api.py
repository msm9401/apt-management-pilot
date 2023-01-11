import requests
import xmltodict
import json


def apt_list(sido):

    """
    시도코드를 이용해 단지 코드, 단지명을 조회할 수 있는 공동주택 단지 목록제공
    """

    url = "http://apis.data.go.kr/1613000/AptListService2/getSidoAptList"
    service_dkey = "OaQeNpErXhERfF1MLLky9CTFOg9QOWnv9WeNpSzGgzsZuCScx4YVgZzG7FkBvUb9ltB2hm0IqnSd87GZF3PPSg=="
    params = {
        "serviceKey": service_dkey,
        "sidoCode": sido,
        "pageNo": 1,
        "numOfRows": "1",
    }

    response = requests.get(url, params=params)
    xml_data = response.content.decode("utf-8")
    parse_data = xmltodict.parse(xml_data)
    json_data = json.loads(json.dumps(parse_data))
    # print(json_data)

    rows = json_data["response"]["body"]["totalCount"]
    print(f"단지 코드 수: {int(rows):,} 개")

    pages = int(int(rows) / 100) + 1
    print(f"pages: {pages}")

    row_count = 1
    apt_list_data = []
    for i in range(1, pages + 1):
        params = {
            "serviceKey": service_dkey,
            "sidoCode": sido,
            "pageNo": i,
            "numOfRows": "100",
        }
        response = requests.get(url, params=params)
        # print(response.content)

        xml_data = response.content.decode("utf-8")
        # print(xml_data)

        parse_data = xmltodict.parse(xml_data)
        # print(parse_data)

        order_data = parse_data["response"]["body"]["items"]["item"]
        print(order_data)
        print(f'page: {i} End\n{"=" * 50}')

        try:
            json_data = json.loads(json.dumps(order_data))
            for code_data in json_data:
                print(f"row_count: {row_count}\n{code_data}\n")
                apt_list_data.append(code_data)
                row_count += 1
        except Exception as e:
            print(f"Error: {e}\n")
            break

    return apt_list_data


# sido_code = 50
# apt_list(sido_code)
