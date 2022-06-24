from captcha.fields import CaptchaTextInput


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'core/custom_field.html'
