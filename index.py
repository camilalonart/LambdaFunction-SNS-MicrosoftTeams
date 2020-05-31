{\rtf1\ansi\ansicpg1252\cocoartf2512
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from __future__ import print_function\
\
import json\
import os\
import urllib3\
\
def send_message(webhook, subject, text, icon, facts, connect=3, read=30):\
    icons = \{\}\
    icons["Check"] = "https://image.flaticon.com/icons/svg/463/463574.svg"\
    icons["Fail"] = "https://image.flaticon.com/icons/svg/463/463612.svg"\
\
    try:\
        image = icons[icon]\
    except KeyError:\
        image = "https://image.flaticon.com/icons/svg/334/334047.svg"\
    \
    headers = \{\}\
    headers['Content-Type'] = 'application/json'\
    parameters = \{\
        "@type": "MessageCard",\
        "@context": "http://schema.org/extensions",\
        "themeColor": "0076D7",\
        "summary": subject,\
        "sections": [\{\
            "activityTitle": "![TestImage](https://www.kaszek.com/wp-content/uploads/2019/08/chiper-logo.png)\{\}".format(subject),\
            "activityText": text,\
            "activityImage": image,\
            "activitySubtitle": "Chiper - Pedido",\
            "facts": facts\
        \}],\
    \}\
\
    encoded_parameters = json.dumps(parameters).encode('utf-8')\
    http = urllib3.PoolManager(timeout = urllib3.Timeout(connect=connect, read=read))\
    try:\
        res = http.request(\
                'POST',\
                webhook,\
                body = encoded_parameters,\
                headers = headers\
            )\
    except (urllib3.exceptions.MaxRetryError,\
            urllib3.exceptions.ConnectTimeoutError,\
            urllib3.exceptions.ReadTimeoutError) as e:\
        print("Microsoft Teams API Error: \{\}".format(e))\
        return\
\
    try:\
        res = json.loads(res.data.decode('utf-8'))\
        return res.status\
    except AttributeError:\
        return\
\
\
def lambda_handler(event, context):\
    print("Received event: " + json.dumps(event, indent=2))\
    message = json.loads(event['Records'][0]['Sns']['Message'])\
    subject = event['Records'][0]['Sns']['Subject']\
    \
    try:\
        text = message['description']\
    except KeyError:\
        text = "N/A"\
        \
    try:\
        icon = message['icon']\
    except KeyError:\
        icon = "default"\
        \
    try:\
        facts = message['facts']\
    except KeyError:\
        facts = []\
        \
    try:\
        webhook = os.environ["teamsKey"]\
    except KeyError:\
        print("ERROR: MSTEAMS_WEBHOOK_URL required in environment.")\
        exit() \
    \
    send_message(webhook, subject, text, icon, facts)\
\
    return message\
}