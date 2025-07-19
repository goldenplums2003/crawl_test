from DrissionPage import Chromium
from CaptchaSolver import CaptchaSolver

browser = Chromium()
tab = browser.latest_tab
# tab.get('https://captcha2.scrape.center/')
# tab.get('https://captcha3.scrape.center/')
# tab.get('https://captcha4.scrape.center/')
# tab.get('https://captcha5.scrape.center/')
tab.get('https://captcha6.scrape.center/')

name = tab.ele('t:input@@type=text@@class=el-input__inner')
password = tab.ele('t:input@@type=password')

name.input('admin')
password.input('admin')

login_button = tab.ele('t:button@@type=button')

tab.wait(4)
login_button.click()
# time.sleep(1)
# login_button.click()

# time.sleep(3)
tab.wait.ele_displayed('t:div@@class=geetest_panel_next', timeout=10)
tab.wait(2)
captcha_panel = tab.ele('t:div@@class=geetest_panel_next')
# print(captcha_panel)

location = captcha_panel.rect.location
size = captcha_panel.rect.size

print(size,location)

captcha_panel.get_screenshot('captcha_panel.png')

captcha_img_path = 'captcha_panel.png'
width = size[0]
height = size[1]

CaptchaSolver = CaptchaSolver()
raw_list = CaptchaSolver.ask_doubao_click_captcha(captcha_img_path)
CaptchaSolver.close()
print(raw_list)

for point in raw_list:
    x, y = point
    x, y = (width/1000) * x, (height/1000) * y
    abs_x = location[0] + x
    abs_y = location[1] + y
    tab.actions.move_to((abs_x, abs_y)).click()
    print(f"Clicked at: ({abs_x}, {abs_y})")
    tab.wait(0.5)
    
tab.ele('t:div@@class=geetest_commit_tip').click()

