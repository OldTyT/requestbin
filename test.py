import msgpack

def from_byte(obj):
    new_obj = {}
    for key, value in obj.items():
        if isinstance(key, bytes):
            key = key.decode("utf-8")
        if isinstance(value, bytes):
            value = value.decode("utf-8")
        new_obj[key] = value
    return new_obj

q = b"\x87\xa7created\xcbA\xd9M\xf6`\x87\x13\xce\xa7private\xc2\xa5color\x93n<\xcc\xfa\xa4name\xa81xr2o19z\xabfavicon_uri\xda\x00edata:image/gif;base64,R0lGODlhEAAQAIAAb'AG48+gAA'ACH5BAQAAAAALAAAAAAQABAAAAIOhI+py+0Po5y02ouzPgUAOw==\xa8requests\x91\xda\x02\xc8\x8b\xa2id\xa629317i\xa4time\xcbA\xd9M\xf6`\x88:\x93\xabremote_addr\xaa172.17.0.1\xa6method\xa3GET\xa7headers\x8a\xa4Host\xaf172.17.0.2:8000\xaaConnection\xaakeep-alive\xb9Upgrade-Insecure-Requests\xa11\xa3Dnt\xa11\xaaUser-Agent\xda\x00eMozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36\xa6Accept\xda\x00\x91text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\xa7Referer\xb7http://172.17.0.2:8000/\xafAccept-Encoding\xadgzip, deflate\xafAccept-Language\xaeen-US,en;q=0.9\xa6Cookie\xda\x00mtoken=9dd302e990ccfb728bc17a378e4239dd5c04fd0d; session=eyJyZWNlbnQiOltdfQ.ZTbdhA.iBhszuq2kkRpU3uj3yO0WwHCBYc\xacquery_string\x81\xa7inspect\xa0\xa9form_data\x90\xa4body\xa0\xa4path\xa9/1xr2o19z\xaccontent_type\xa0\xaecontent_length\x00\xaasecret_key\xc0"
q = msgpack.loads(q)
print(from_byte(q))
