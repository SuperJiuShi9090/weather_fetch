"""
此文件存放各种API的json解析的函数，解析结果仅供参考！
此为解析示例
"""
from LOG import *
from dictionary import *

logger = logging.getLogger(__name__)

def warjs(js) -> list:#实时预警json解析
    data=js["metadata"]
    atrbut = data.get("attributions",None)          # 取不到返回 None
    if atrbut is not None:
        a = ""
        for i in atrbut:
            a += i+"\n"
        atrb = "声明：数据来自" + a
    else:
        atrb = None
    lice = "="*20+"\n数据来源：和风天气API"
    if data["zeroResult"] is False:
        dtl = js["alerts"][0]
        sdnm = ("预报机构："+dtl.get("senderName",None)) if a else None
        #istm = "生成时间："+dtl["issuedTime"]
        
        mstp = dtl["messageType"]
        if mstp["code"] == "alert":
            mstp = "/////持续有效的初始信息！/////"
        elif mstp["code"] == "update":
            mstp = "/////更新过的预警信息！/////"
        elif mstp["code"] == "cancle":
            mstp = "预警已取消！暂无预警uwu"
            return ["",sdnm,mstp,"","","","","","",lice]
        
        urgc = dtl["urgency"]
        if urgc == "immediate":
            urgc = "必须立刻采取行动！"
        elif urgc == "expected":
            urgc = "应尽快采取行动（通常在 1 小时内）！"
        elif urgc == "future":
            urgc = "应在近期采取行动！"
        elif urgc == "past":
            urgc = "事件已不再发生。"
        elif urgc == "unknown":
            urgc = "紧迫性未知！"
        else:
            urgc = None
        
        svrt = dtl["severity"]
        if svrt == "unknown":
            svrt = "提示：严重性未知！"
        elif svrt == "minor":
            svrt ="提示：对生命或财产构成的威胁极小或没有已知威胁。"
        elif svrt == "moderate":
            svrt = "提示：对生命或财产可能构成威胁！"
        elif svrt == "severe":
            svrt = "提示：对生命或财产构成的重大威胁！"
        elif svrt == "extreme":
            svrt = "提示：对生命或财产构成的严重威胁！"
        
        cett = dtl["certainty"]
        if cett == "observed":
            cett = "可能性：事件已经发生或正在发生。"
        elif cett == "likely":
            cet ="可能性；发生概率大于约 50%"
        elif cett == "unlikely":
            cett = "可能性：预计不会发生（概率接近 0）"
        elif cett == "unknown":
            cett = "可能性：确定性未知！"
        else:
            cett = None
        
        if urgc and cett is not None:
            cett += urgc
        elif cett is None and urgc is not None:
            cett = urgc
        ic = icon.get(dtl["icon"],"")
        tpnm = dtl["eventType"]["name"]
        colo = dtl["color"]
        if colo["code"] == "white":
            colo = tpnm + "白色预警"
        elif colo["code"] == "gray":
            colo = tpnm + "灰色预警"
        elif colo["code"] == "green":
            colo = "💚"#tpnm + 绿色预警
        elif colo["code"] == "blue":
            colo = "💙"#tpnm + 蓝色预警
        elif colo["code"] == "yellow":
            colo = "💛"#tpnm + 黄色预警
        elif colo["code"] == "amber":
            colo = tpnm + "琥珀色预警"
        elif colo["code"] == "orange":
            colo = "🧡"#橙色预警
        elif colo["code"] == "red":
            colo = "❤️"#红色预警
        elif colo["code"] == "purple":
            colo = "💜"#紫色预警
        elif colo["code"] == "black":
            colo = "🖤"#黑色预警
        else: colo = ""
        colo += ic
        #eftm = "预警生效时间："+dtl.get("effectiveTime",None)
        #ostm = "预警开始时间："+dtl.get("onsetTime",None)
        #eptm = "预警失效时间："+dtl["expireTime"]
        hdln = "标题："+dtl["headline"]+colo
        dcpt = "详细信息："+dtl["description"]
        istt = "防御指南：\n"+dtl.get("instruction",None)
        return [hdln,sdnm,mstp,dcpt,svrt,cett,istt,atrb,lice]
    else:
        return [None,"","","","","","","","",lice]

def weajs(js, rsp="1") -> list:
    """
    天气预报解析，返回列表，天气行格式：天气：🌤多云
    rsp=1 当前 / 2 逐小时 / 3 逐日
    """
    if rsp == "1":
        Data = [js['now']]
    elif rsp == "2":
        Data = js['hourly']
    elif rsp == "3":
        Data = js['daily']
    else:
        Data = []

    lines = []
    lice = "="*20 + "\n数据来源：和风天气API"

    for item in Data:
        for k, v in item.items():
            cn   = WEA.get(k)
            unit = WEAunit.get(k)
            if cn is None:
                continue

            # 天气类字段特殊处理
            if k == "text":
                ic = item.get("icon", "")
                lines.append(f"{cn}：{icon.get(ic, '')}{v}")
            elif k == "textDay":
                ic = item.get("iconDay", "")
                lines.append(f"白天：{icon.get(ic, '')}{v}")
            elif k == "textNight":
                ic = item.get("iconNight", "")
                lines.append(f"夜晚：{icon.get(ic, '')}{v}")
            else:
                # 非天气字段保持原样
                lines.append(f"{cn}：{v}{unit}")

    lines.append(lice)
    return lines

def ctaqijs(j):
    #tag   = j["metadata"]["tag"]
    indexes = j["indexes"][0]          # 只取第一条综合指数
    #polls   = j["pollutants"]          # 各污染物列表
    stations = j["stations"]           # 监测点列表
    
    # 2. 综合指数硬编码
    primary  = indexes.get("primaryPollutant",None)
    if primary is not None:
        primary = indexes["primaryPollutant"]["name"]  # "PM 10"
        prmr = "首要污染 :" + primary
    else:
        prmr = None
    
    aqi = "AQI      :" + str(indexes["aqi"])
    leve = "等级     :" + indexes["level"]
    ctgr = "类别     :" + indexes["category"]
    efct = "影响     :" +  indexes["health"]["effect"]
    adgn = "一般人群 :" + indexes["health"]["advice"]["generalPopulation"]
    adsn = "敏感人群 :" + indexes["health"]["advice"]["sensitivePopulation"]
    
    """
    for p in polls:
        code  = p["code"]                       # pm2p5 / pm10 / no2 ...
        name  = p["name"]                       # PM 2.5 / PM 10 / NO2 ...
        value = p["concentration"]["value"]     # 浓度数值
        unit  = p["concentration"]["unit"]      # μg/m³ 或 mg/m³
        sub   = p["subIndexes"][0]["aqi"]       # 分指数
        print(f"{name:<4} 浓度={value:6.2f}{unit:<6} 分指数={sub}")
    """
    sdnm = "监测点 :"
    for i in stations:
        sdnm += i["name"]+" "
    lice = "="*20+"\n数据来源：和风天气API"
    return [aqi,leve,ctgr,prmr,efct,adgn,adsn,sdnm,lice]

def hlaqijs():
    ...

def dlaqijs(js):
    data = js["days"]
    sttm1 = data[0]["forecastStartTime"]
    edtm1 = data[0]["forecastEndTime"]


if __name__ == "__main__":
    logger.info("json解析测试")
    from GEO_API import location_info as locINFO
    name,ID,lat,lon = locINFO("南京")
    
    from API import *
    data = war(lat, lon)
    cnt1=warjs(data)
    if cnt1[0] is not None:
        for i in cnt1:
            if i is not None:
                print(i)
    else:
        print(name+"暂时还没有预警信息哦～")
    """
    cnt2=weajs(wea(weatherurl(ID,"3"),name),rsp="3")
    for i in cnt2:
        print(i)
    
    url = aqiurl(lat,lon,ans="4")
    cont = aqi(url,name)
#    print(cont)
    for i in ctaqijs(cont):
        if i is not None:
            print(i)
    """
    logger.info("json解析测试结束")
    
