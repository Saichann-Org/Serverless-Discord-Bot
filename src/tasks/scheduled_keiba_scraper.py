import os
import requests
from bs4 import BeautifulSoup
import time
import boto3
from datetime import datetime

# DynamoDBリソースを作成
dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-northeast-1'
)
race_table = dynamodb.Table('RaceData')
payback_table = dynamodb.Table('PaybackData')

def save_data_to_dynamodb(horse_info, race_info, payback_info, race_id):
    for horse_name, jockey, finish_position, horse_number, runtime, odds, pas, weight, sex_old, handi, last, pop in zip(*horse_info):
        item = {
            'RaceID': race_id,
            'RaceTitle': race_info['RaceTitle'],
            'RaceDate': race_info['RaceDate'],
            'Surface': race_info['Surface'],
            'Distance': race_info['Distance'],
            'Round': race_info['Round'],
            'Condition': race_info['Condition'],
            'Weather': race_info['Weather'],
            'Class': race_info['Class'],
            'Detail': race_info['Detail'],
            'HorseName': horse_name,
            'Jockey': jockey,
            'FinishPosition': finish_position,
            'HorseNumber': horse_number,
            'Runtime': runtime,
            'Odds': odds,
            'PassingOrder': pas,
            'Weight': weight,
            'SexOld': sex_old,
            'Handicap': handi,
            'LastTime': last,
            'Popularity': pop,
        }
        race_table.put_item(Item=item)

    # 払い戻し情報を保存
    payback_item = {
        'RaceID': race_id,
        'PaybackInfo': {
            'win': payback_info[0] if len(payback_info) > 0 else None,
            'place': payback_info[1] if len(payback_info) > 1 else None,
            'exacta': payback_info[2] if len(payback_info) > 2 else None,
            'quinella_place': payback_info[3] if len(payback_info) > 3 else None,
            'trifecta': payback_info[4] if len(payback_info) > 4 else None,
            'trio': payback_info[5] if len(payback_info) > 5 else None,
            'triple': payback_info[6] if len(payback_info) > 6 else None,
        }
    }
    payback_table.put_item(Item=payback_item)

# スクレイピング処理
year = "2022"  # 西暦を入力

def appendPayBack1(varSoup):  # 複勝とワイド以外で使用
    varList = []
    varList.append(varSoup.contents[3].contents[0])
    varList.append(varSoup.contents[5].contents[0])
    payBackInfo.append(varList)

def appendPayBack2(varSoup):  # 複勝とワイドで使用
    varList = []
    for var in range(3):
        try:  # 複勝が3個ないときを除く
            varList.append(varSoup.contents[3].contents[2 * var])
        except IndexError:
            pass
        try:
            varList.append(varSoup.contents[5].contents[2 * var])
        except IndexError:
            pass
    payBackInfo.append(varList)

def lambda_handler(event, context):
    List = []
    domin = "https://db.netkeiba.com/race/"
    l = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]  # 競馬場
    for w in range(len(l)):
        for z in range(8):  # 開催、6まで十分だけど保険で7
            for y in range(16):  # 日、12まで十分だけど保険で14
                yBreakCounter = 0  # yの更新をbreakするためのカウンター
                for x in range(13):  # レース12
                    url = year + l[w] + "0" + str(z + 1) + str(y + 1).zfill(2)  + str(x + 1).zfill(2)
                    r = requests.get(domin + url)
                    time.sleep(1)  # サーバーの負荷を減らすため1秒待機する
                    soup = BeautifulSoup(r.content.decode("euc-jp", "ignore"), "html.parser")  # バグ対策でdecode
                    soup_span = soup.find_all("span")
                    allnum = (len(soup_span) - 6) / 3  # 馬の数
                    if allnum < 1:  # urlにデータがあるか判定
                        yBreakCounter += 1
                        break
                    allnum = int(allnum)
                    
                    # 馬の情報
                    soup_txt_l = soup.find_all(class_="txt_l")
                    name = []  # 馬の名前
                    for num in range(allnum):
                        name.append(soup_txt_l[4 * num].contents[1].contents[0])

                    jockey = []  # 騎手の名前
                    for num in range(allnum):
                        jockey.append(soup_txt_l[4 * num + 1].contents[1].contents[0])

                    soup_txt_r = soup.find_all(class_="txt_r")
                    
                    finish_position = []  # 着順
                    for num in range(allnum):
                        finish_position.append(soup_txt_r[5 * num].contents[0])
                    
                    horse_number = []  # 馬番
                    for num in range(allnum):
                        horse_number.append(soup_txt_r[1 + 5 * num].contents[0])

                    runtime = []  # 走破時間
                    for num in range(allnum):
                        try:
                            runtime.append(soup_txt_r[2 + 5 * num].contents[0])
                        except IndexError:
                            runtime.append(None)

                    odds = []  # オッズ
                    for num in range(allnum):
                        odds.append(soup_txt_r[3 + 5 * num].contents[0])

                    soup_nowrap = soup.find_all("td", nowrap="nowrap", class_=None)
                    pas = []  # 通過順
                    for num in range(allnum):
                        try:
                            pas.append(soup_nowrap[3 * num].contents[0])
                        except:
                            pas.append(None)

                    weight = []  # 体重
                    for num in range(allnum):
                        weight.append(soup_nowrap[3 * num + 1].contents[0])

                    soup_tet_c = soup.find_all("td", nowrap="nowrap", class_="txt_c")
                    sex_old = []  # 性齢
                    for num in range(allnum):
                        sex_old.append(soup_tet_c[6 * num].contents[0])

                    handi = []  # 斤量
                    for num in range(allnum):
                        handi.append(soup_tet_c[6 * num + 1].contents[0])

                    last = []  # 上がり
                    for num in range(allnum):
                        try:
                            last.append(soup_tet_c[6 * num + 3].contents[0].contents[0])
                        except IndexError:
                            last.append(None)

                    pop = []  # 人気
                    for num in range(allnum):
                        try:
                            pop.append(soup_span[3 * num + 10].contents[0])
                        except IndexError:
                            pop.append(None)

                    horse_info = [name, jockey, finish_position, horse_number, runtime, odds, pas, weight, sex_old, handi, last, pop]

                    # レースの情報
                    try:
                        var = soup_span[8]
                        sur = str(var).split("/")[0].split(">")[1][0]
                        rou = str(var).split("/")[0].split(">")[1][1]
                        dis = str(var).split("/")[0].split(">")[1].split("m")[0][-4:]
                        con = str(var).split("/")[2].split(":")[1][1]
                        wed = str(var).split("/")[1].split(":")[1][1]
                    except IndexError:
                        try:
                            var = soup_span[7]
                            sur = str(var).split("/")[0].split(">")[1][0]
                            rou = str(var).split("/")[0].split(">")[1][1]
                            dis = str(var).split("/")[0].split(">")[1].split("m")[0][-4:]
                            con = str(var).split("/")[2].split(":")[1][1]
                            wed = str(var).split("/")[1].split(":")[1][1]
                        except IndexError:
                            var = soup_span[6]
                            sur = str(var).split("/")[0].split(">")[1][0]
                            rou = str(var).split("/")[0].split(">")[1][1]
                            dis = str(var).split("/")[0].split(">")[1].split("m")[0][-4:]
                            con = str(var).split("/")[2].split(":")[1][1]
                            wed = str(var).split("/")[1].split(":")[1][1]
                    
                    soup_smalltxt = soup.find_all("p", class_="smalltxt")
                    detail = str(soup_smalltxt).split(">")[1].split(" ")[1]
                    date = str(soup_smalltxt).split(">")[1].split(" ")[0]
                    clas = str(soup_smalltxt).split(">")[1].split(" ")[2].replace(u'\xa0', u' ').split(" ")[0]
                    title = str(soup.find_all("h1")[1]).split(">")[1].split("<")[0]
                    race_info = {
                        'RaceTitle': title,
                        'RaceDate': date,
                        'Detail': detail,
                        'Class': clas,
                        'Surface': sur,
                        'Distance': dis,
                        'Round': rou,
                        'Condition': con,
                        'Weather': wed
                    }

                    # RaceIDの生成: YYYYMMDD{競馬場}{レース番号}
                    date = datetime.strptime(date, '%Y年%m月%d日')
                    race_id = url

                    # 払い戻しの情報
                    payBack = soup.find_all("table", summary='払い戻し')
                    payBackInfo = []  # 単勝、複勝、枠連、馬連、ワイド、馬単、三連複、三連単の順番で格納
                    appendPayBack1(payBack[0].contents[1])  # 単勝
                    try:
                        payBack[0].contents[5]  # これがエラーの時複勝が存在しない
                        appendPayBack2(payBack[0].contents[3])  # 複勝
                        try:
                            appendPayBack1(payBack[0].contents[7])  # 馬連
                        except IndexError:
                            appendPayBack1(payBack[0].contents[5])  # 通常は枠連だけど、この時は馬連
                    except IndexError:  # この時複勝が存在しない
                        payBackInfo.append([payBack[0].contents[1].contents[3].contents[0], '110'])  # 複勝110円で代用
                        print("複勝なし")
                        appendPayBack1(payBack[0].contents[3])  # 馬連
                    appendPayBack2(payBack[1].contents[1])  # ワイド
                    appendPayBack1(payBack[1].contents[3])  # 馬単
                    appendPayBack1(payBack[1].contents[5])  # 三連複
                    try:
                        appendPayBack1(payBack[1].contents[7])  # 三連単
                    except IndexError:
                        appendPayBack1(payBack[1].contents[5])  # 三連複を三連単の代わり

                    # データをDynamoDBに保存
                    save_data_to_dynamodb(horse_info, race_info, payBackInfo, race_id)

                    print(detail + str(x + 1) + "R")  # 進捗を表示
                    
                if yBreakCounter == 12:  # 12レース全部ない日が検出されたら、その開催中の最後の開催日と考える
                    break

    print("終了")
