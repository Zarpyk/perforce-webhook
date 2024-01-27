import os
import subprocess
import time
import pickle
from datetime import datetime, timezone
from discord_webhooks import DiscordWebhooks

class PerforceLogger():
    def __init__(self, webhook_url):
      """ Initializes a 30 second timer used to check if commits have been made.  """
      self.webhook_url = webhook_url
      self.latest_change = ""
      self.save_file = "save.p"
      if not os.path.exists(self.save_file):
        os.mknod(self.save_file)

    def check_p4(self):
      """ Runs the p4 changes command to get the latest commits from the server. """
      p4_changes = subprocess.Popen('p4 changes -t -m 1 -l', stdout=subprocess.PIPE, shell=True)
      return p4_changes.stdout.read().decode('ISO-8859-1')

    def check_for_changes(self, output):
      """ Figures out if the latest p4 change is new or should be thrown out. """
      if os.path.getsize(self.save_file) > 0:
        self.latest_change = pickle.load(open(self.save_file, "rb"))
      if output != self.latest_change:
        pickle.dump(output, open(self.save_file, "wb"))

        if '*pending*' in output: 
          return ''

        else:
          return output

      else: 
        return ''

    def post_changes(self):
      """ Posts the changes to the Discord server via a webhook. """
      output = self.check_p4()
      print("Output: %s" % output)
      if output == '':
        return
      payload = self.check_for_changes(output)
      print("Latest Change: %s" % self.latest_change)
      if payload != '':
        payload_title, payload_description = payload.split('\n', maxsplit=1)
        payload_title = payload_title.replace("Change ", "Change #")
        payload_description = payload_description.lstrip()
        
        position_on = payload_title.find("on") + 3
        position_by = payload_title.find("by")
        date = payload_title[position_on:position_by].strip()
        payload_title = payload_title.replace(" on " + date, "")
        
        date_format = datetime.strptime(date, "%Y/%m/%d %H:%M:%S")
        date_utc = date_format.replace(tzinfo=timezone.utc)
        date = date_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        lines = payload_description.split('\n')
        lines = [line for line in lines if line.strip() != '']
        formatted_lines = [f"> {line}" for line in lines]
        payload_description = '\n'.join(formatted_lines)
        
        message = DiscordWebhooks(self.webhook_url)
        message.set_content(color=0x4aff48, description='%s' % (payload_description), timestamp='%s' % date)
        message.set_author(name='%s' % payload_title)
        message.set_footer(text='From 0.0.0.0 Perforce Server', ts=True)
        message.send()

      else:
        return

if __name__ == "__main__":
  """ Initializes the application loop that checks Perforce for changes. """
  DISCORD_WEBHOOK_URL = "https://ptb.discord.com/api/webhooks/link"
  logger = PerforceLogger(DISCORD_WEBHOOK_URL)
  timer = time.time()

  while True:
    logger.post_changes()
    time.sleep(10.0 - ((time.time() - timer) % 10.0))