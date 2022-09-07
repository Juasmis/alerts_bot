# Alerts API and db
import argparse
from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel
import uvicorn
import json
import random
import httpx
import argparse

app = FastAPI()
    
# API model
class alert_item(BaseModel):
    level: str
    title: str
    message: str
    source: str

# Program input arguments
parser = argparse.ArgumentParser()
# Opcional. Nombre del archivo de configuración a usar
parser.add_argument("-f","--conf_file", help="Configuration file name",
                    required=False, type=str, default='config_alerts_bot.json')
args = parser.parse_args()

# Read configuration file
with open(args.conf_file, mode="r", encoding='utf-8') as file: 
    config = json.loads(file.read())
    
# API endpoint that receives the alerts
@app.post("/generate_alert")
async def generate_message(request: Request, alert_data: alert_item):
    # print(alert_data.level.lower())
    if alert_data.level.lower() not in config["alerts"]:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="Invalid alert level, valid levels are: " + ", ".join(config["alerts"].keys()))
    
    # Select a randon media file from the list
    media_dict = config['alerts'][alert_data.level.lower()]['file_ids']
    media = list( media_dict.keys() )
    media_item = media_dict[media[random.randint(0, len(media) - 1)]]
    
    # Prepare the message
    text = f"""*Level*: {alert_data.level} 
*{alert_data.title}*
{alert_data.message}

*Source*: {alert_data.source}""".replace('_', '\_')

    # Finally, send the message in every chat where the bot is present
    for chat_id in config['chat_ids']:
        httpx.post(f'https://api.telegram.org/bot{config["token"]}/sendAnimation', 
                    data={'chat_id': chat_id,
                          'animation': media_item,
                          'caption':text,
                          'parse_mode': 'MarkdownV2'
                          }
                    )

if __name__ == '__main__':
        uvicorn.run(app, host="0.0.0.0", port=config['port'])