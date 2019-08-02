# coding: utf-8

from django import forms


class WeixinOptionsForm(forms.Form):
    access_token = forms.CharField(
        max_length=255,
        help_text='WexinTalk robot access_token'
    )
