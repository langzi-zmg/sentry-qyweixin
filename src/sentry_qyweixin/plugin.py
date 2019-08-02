# coding: utf-8

import json

import requests
from sentry.plugins.bases.notify import NotificationPlugin

import sentry_qyweixin
from .forms import WeixinOptionsForm

DingTalk_API = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={access_token}"


class QyWeixinPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to DingDing.
    """
    author = 'ansheng'
    author_url = 'https://github.com/anshengme/sentry-dingding'
    version = sentry_qyweixin.VERSION
    description = 'Send error counts to DingDing.'
    resource_links = [
        ('Source', 'null'),
        ('Bug Tracker', 'null'),
        ('README', 'null'),
    ]

    slug = 'QyWeixin'
    title = 'QyWeixin'
    conf_key = slug
    conf_title = title
    project_conf_form = WeixinOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('access_token', project))

    def notify_users(self, group, event, *args, **kwargs):
        self.post_process(group, event, *args, **kwargs)

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        access_token = self.get_option('access_token', group.project)
        send_url = DingTalk_API.format(access_token=access_token)
        title = "New alert from {}".format(event.project.slug)

        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": u"#### {title} \n > {message} [href]({url})".format(
                    title=title,
                    message=event.message,
                    url=u"{}events/{}/".format(group.get_absolute_url(), event.id),
                )
            }
        }
        requests.post(
            url=send_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8")
        )
