class CaptchaSolver:
    def __init__(self):
        self.browser = None
        self.tab = None

    def ask_gpt_captcha(self, captcha_img_path, width, height):
        from DrissionPage import Chromium

        self.browser = Chromium()
        self.tab = self.browser.new_tab('https://chat.openai.com/')

        self.tab.wait.load_start()
        self.tab.wait(5)

        attach_button = self.tab.ele('t:button@@id=upload-file-btn')
        if attach_button:
            attach_button.click()
            self.tab.wait(1)
            
            img_attach_button = self.tab.ele('t:div@@class=truncate@@text()=添加照片和文件')
            
            img_attach_button.click.to_upload(captcha_img_path)
            self.tab.wait(1)

        else:
            print('未找到上传按钮')

        self.tab.wait(3)

        text_box = self.tab.ele('xpath://textarea')
        if text_box:
            question = f"这张图片的宽和高分别是{width}和{height}，请根据图片中上方文字的要求，给出需要点击的坐标，坐标格式为[(x1,y1),(x2,y2),(x3,y3)]，其中，每个元组中的内容是具体的坐标位置，列表中的元组的数量与顺序对应图片中的文字要求。如：[(23,65),(76,32)]。请不要输出任何其他内容。"
            text_box.input(question)
            self.tab.wait(1)

            send_button = self.tab.ele('t:button@@id=composer-submit-button')
            if send_button:
                send_button.click()
            else:
                print('未找到发送按钮')
        else:
            print('未找到输入框')
        

        self.tab.wait(5)

        text = self.tab.ele('xpath:(//div[contains(@class, "markdown")])[last()]').text
        print(text)
        
        return text
    
    def ask_doubao_click_captcha(self, captcha_img_path):
        from DrissionPage import Chromium
        import re

        self.browser = Chromium()
        self.tab = self.browser.new_tab('https://www.doubao.com/chat/')

        self.tab.wait.load_start()
        # self.tab.wait(2)

        attach_button = self.tab.ele('t:button@@data-testid=upload_file_button')
        if attach_button:
            attach_button.click()
            # self.tab.wait(1)
            
            img_attach_button = self.tab.ele('t:div@@data-testid=upload_file_panel_upload_item')
            if img_attach_button:
                img_attach_button.click.to_upload(captcha_img_path)
                # self.tab.wait(1)
            else:
                print('未找到文件输入框')
        else:
            print('未找到上传按钮')

        self.tab.wait(3)

        text_box = self.tab.ele('xpath://textarea')
        if text_box:
            question = f"如果图片整体左上角坐标为(0,0)，右下角坐标为(1000,1000)，依照这个比例，请根据图片中上方文字的要求，给出需要点击的坐标，坐标格式为[(x1,y1),(x2,y2),(x3,y3)]，其中，每个元组中的内容是具体的坐标位置，列表中的元组的数量与顺序对应图片中的文字要求，输出的坐标需为整数。请不要输出任何其他内容，只输出坐标本身！回答示例：[(x1,y1),(x2,y2)]。"
            text_box.input(question)
            # self.tab.wait(1)

            send_button = self.tab.ele('t:button@@aria-label=发送')
            send_button.click()
        else:
            print('未找到输入框')

        stop_generating_button = self.tab.ele('t:div@@data-testid=chat_input_local_break_button')
        
        while True:
            stop_generating_button = self.tab.ele('t:div@@data-testid=chat_input_local_break_button')
            if stop_generating_button and '!hidden' not in stop_generating_button.attr('class'):
                print('class changed from hidden to visible')
                break
            self.tab.wait(0.5)
            
        while True:
            stop_generating_button = self.tab.ele('t:div@@data-testid=chat_input_local_break_button')
            if stop_generating_button and '!hidden' in stop_generating_button.attr('class'):
                print('class changed from visible to hidden')
                break
            self.tab.wait(0.5)
            
        print('Answer completed!')


        messages = self.tab.eles('t:div@@data-testid=message_text_content')
        last_message= messages[-1].text
        print(f"The answer of doubao is: {last_message}")

        pattern = r'\[\(\d+,\s*\d+\)(?:,\s*\(\d+,\s*\d+\))*\]'
        matches = re.findall(pattern, last_message)
        # print(matches)
        
        coordinate_lists = []
        for match in matches:
            try:
                cleaned = match.replace(' ', '')
                coord_list = eval(cleaned)
                if isinstance(coord_list, list):
                    coordinate_lists.append(coord_list)
            except:
                continue
        
        if coordinate_lists:
            result_list = coordinate_lists[-1]
        else:
            result_list = []

        return result_list
    
    def ask_doubao_input_captcha(self, captcha_img_path):
        from DrissionPage import Chromium
        import re

        self.browser = Chromium()
        self.tab = self.browser.new_tab('https://www.doubao.com/chat/')

        self.tab.wait.load_start()
        # self.tab.wait(2)
        
        attach_button = self.tab.ele('t:button@@data-testid=upload_file_button')
        if attach_button:
            attach_button.click()
            # self.tab.wait(1)
            
            img_attach_button = self.tab.ele('t:div@@data-testid=upload_file_panel_upload_item')
            if img_attach_button:
                img_attach_button.click.to_upload(captcha_img_path)
                # self.tab.wait(1)
            else:
                print('未找到文件输入框')
        else:
            print('未找到上传按钮')

        self.tab.wait(3)

        text_box = self.tab.ele('xpath://textarea')
        if text_box:
            question = f"判断这张图片上的字符是什么(只可能是四个大小写字母或数字)，请直接输入字符内容，不要带空格，不要输出任何其他内容！"
            text_box.input(question)
            # self.tab.wait(1)

            send_button = self.tab.ele('t:button@@aria-label=发送')
            send_button.click()
        else:
            print('未找到输入框')
        
        self.tab.wait(5)
            
        print('Answer completed!')

        messages = self.tab.eles('t:div@@data-testid=message_text_content')
        last_message= messages[-1].text
        print(f"The answer of doubao is: {last_message}")

        return last_message

    def close(self):
        if self.tab:
            self.tab.close()

if __name__ == '__main__':
    solver = CaptchaSolver()
    result = solver.ask_doubao_click_captcha('captcha_panel.png')
