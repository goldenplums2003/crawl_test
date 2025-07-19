from DrissionPage import Chromium
from CaptchaSolver import CaptchaSolver

browser = Chromium()
tab = browser.latest_tab
# tab.get('https://captcha7.scrape.center/')
tab.get('https://captcha8.scrape.center/')

name = tab.ele('t:input@@type=text@@class=el-input__inner')
password = tab.ele('t:input@@type=password')

name.input('admin')
password.input('admin')

login_button = tab.ele('t:button@@type=button')

captcha = tab.ele('t:canvas@@id=captcha')

captcha.get_screenshot('captcha_panel.png')

CaptchaSolver = CaptchaSolver()
answer = CaptchaSolver.ask_doubao_input_captcha('captcha_panel.png')
CaptchaSolver.close()

captcha_input_box = tab.ele('x://*[@id="app"]/div[2]/div/div/div/div/div/form/div[3]/div/div/div[1]/div/input')
captcha_input_box.input(answer)

login_button.click()
