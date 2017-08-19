import json
from bittrex.bittrex import Bittrex
import smtplib
import time
from xml.etree.ElementTree import parse


def execute_command(command):
    try:
        response = requests.get(BaseURL + command, timeout = 10);
    except:
        return;

    if response.status_code == 200:
        return json.loads(response.text)
    return;

def load_config(file_name):
    info = {};
    tree = parse(file_name);
    config = tree.getroot();
    alarms_element = config.find('alarms');
    alarms = alarms_element.findall('alarm');
    info['email'] = str(config.findtext('email'));
    info['send_email'] = str(config.findtext('send_email'));
    info['send_password'] = str(config.findtext('send_password'));
    info['info'] = {};
    for alarm in alarms:
        info['info'][alarm.findtext('currency')] = {'high':float(alarm.findtext('high')), 'low':float(alarm.findtext('low')), 'active':True};
    return info;

def send_email(address, msg, sender, password):
    s = smtplib.SMTP_SSL('smtp.gmail.com',465);
    s.login(sender, password);
    s.sendmail(sender, address, msg);
    s.quit();

def check_price(config):
    bittrex = Bittrex(None, None);
    email = config['email'];
    infos = config['info'];
    for key in infos:
        if infos[key]['active']:
            result = bittrex.get_marketsummary(key);
            if result:
                if result['success'] == True:
                    price = result['result'][0]['Last'];
                    high = infos[key]['high'];
                    low = infos[key]['low'];
                    msg = "";
                    if price >= high:
                        msg = "{!s}'s price({:.9f}) is higher than {:.9f}".format(key, price, high);
                    elif price <= low:
                        msg = "{!s}'s price({:.9f}) is lower than {:.9f}".format(key, price, low);
                    else:
                        return;

                    infos[key]['active'] = False;
                    print(msg);
                    send_email(email, msg, config['send_email'], config['send_password']);

            else:
                print(key + "is not exist");

def OutputConfig(config):
    print('email : {!s}'.format(config['email']));
    infos = config['info'];
    for key in infos:
        high = infos[key]['high'];
        low = infos[key]['low'];
        print("{!s} high({:f}) low({:f})".format(key, high, low));

def main():
    print('load config.xml');
    config_info = load_config('config_bittrex.xml');

    OutputConfig(config_info);
    print('start!');

    while True:
        check_price(config_info);
        time.sleep(5);

main();






