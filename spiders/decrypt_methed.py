import os
import sys
envplat_dir = os.path.dirname(os.path.realpath(__file__)).split("spiders")[0]
sys.path.append(envplat_dir + "spiders")
# from base_settings import *
from base_method import *
from log_setting import logger
from login_extra.tool.YDMHTTPDemo3x import YDMHttp


def get_youdao_sign(word, ts, user_agent=''):
    salt = str(ts)+str(random.randint(0,10))
    bv = MD5(user_agent)
    sign = MD5("fanyideskweb" + word + salt + "@6f#X3=cCuncYssPsuRUE")
    return salt, bv, sign


def decrypt_baidu_index_response(keys, encrypt_data):
    """百度指数返回结果解密"""
    w_data = {}
    print(keys)
    for index in range(len(keys)//2):
        w_data[keys[index]] = keys[len(keys)//2 + index]
    print(w_data)
    decrypt_data = ''
    print(encrypt_data)
    for i in range(len(encrypt_data)):
        decrypt_data += w_data[encrypt_data[i]]
    print(decrypt_data)
    return decrypt_data


def get_sougou_weixin_detail_url(url):
    '''搜狗微信，列表页获取的url进行处理，返回真实url'''
    url = url if url.startswith('http') else 'https://weixin.sogou.com' + url
    k_data = random.randint(1, 100)
    h_data = url.index('url=')
    c_data = url.index('&k=') if '&k=' in url else -1
    print(k_data, h_data, c_data)

    if h_data != -1 and c_data == -1:
        h_data = url[h_data+ 30 + k_data:h_data+ 31 + k_data]
        return url + '&k=' + str(k_data) + '&h=' + str(h_data)
    else:
        return url


def str2token(str_data):
    token = ''
    for val in str_data:
        token += str(hex(ord(val)))
    return token.replace('0x', '')

def china_land(url, text):
    """
    中国土地市场网
    :param url: 链接
    :param text: 验证码
    :return:
    """
    cookie = ''
    if "security_verify_" not in url:
        cookie = 'srcurl=' + str2token(url) + ';path=/;'
    url = "http://www.landchina.com/default.aspx?tabid=226&security_verify_img=" + str2token(text)
    return url, cookie

def stringToHex(s):
    val = ""
    for k in s:
        if (val == ""):
            val = str(hex(ord(k)))
        else:
            val += str(hex(ord(k)))
    return val.replace("0x", "")

def get_cookie(url):
    screendate = "1366,768" #  屏幕宽度和高度我们可以设置成固定值．
    curlocation = url  # 当前请求的url
    cookie = "srcurl=" + stringToHex(curlocation) + ";path=/;"
    cookie = {"srcurl": cookie}
    url = url + "&security_verify_data=" + stringToHex(screendate)
    return url, cookie


if __name__ == '__main__':
    # data = decrypt_baidu_index_response("rRP,Gi4XSkAvb1.42,108+95.6-37%", 'SRAXRPSb1bAPSbAAAPS1,irPSbAiGPSRbSAPS,A,APS,bbRPS,ArrPS,SrRPSSASSPSrRRSPSbRS1PSS,,XPSRiSRPSRR,GPSGbR,PSGGAbPSrRRbPSASbSPSSGiiPSS,,bPSrriSPSri1APSSrArPSSAGRPSbSirPSXRGRPSARriPS,bGS')
    # print(data)
    # print(get_sougou_weixin_detail_url('https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6EzDJysI4ql5MPrOUp16838dGRMI7NnPqqmqghgrZjZoAwla_S92HUwwvDqyjOWdzb_UcLpYkX0ABd5cGalMZ82hiRv6K94Zow4jG6WOtmaJceIcIwmExZxIIZrbOZGYWdida8Qgf2vh7OrhA4PNjrWMMdGfWP9xBOPhvugdGMUA52SESmjn9sm4OZCnxixtX&type=1&query=%E4%B8%8A%E6%B5%B7&k=68&h=d'))
    # print(get_sougou_weixin_detail_url('/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6EzDJysI4ql5MPrOUp16838dGRMI7NnPqERBhyS3pkIBJmUnGOsj5sAwvDqyjOWdzMmpGksUKiyE_Tvi0whLU5cCowwMU67tf8tcP0o0o_7IFlfgEmchfFxYpBdjoH0vIIdG2vChq_ChPHT-bnSSlhxnC98UDZYl-klHlKAxTKYxkhZQjSUnUsGRTpLLTNgHY&type=1&query=%E5%8C%97%E4%BA%AC'))
    # print(china_land('http://www.landchina.com/default.aspx?tabid=226'))
    # print(get_cookie('http://www.landchina.com/default.aspx?tabid=226'))
    url = 'https://feeds.m.iqiyi.com/f.html?id=11532260570'
    res_1 = requests.get(url, headers=get_headers())
    html = etree.HTML(res_1.text)
    vid = html.xpath('//div[@id="video"]/@data-tvi')[0]
    video_url = get_haoduo_vf(vid)
    res_2 = requests.get(video_url, headers=get_headers())
    print(res_2.text)
