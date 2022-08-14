from captcha.fields import CaptchaTextInput


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'store/custom_field.html'
