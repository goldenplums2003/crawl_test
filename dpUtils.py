class dpUtils:
    def __init__(self):
        self.browser = None
        self.tab = None
        
    def get_table(self,table_ele):
        # This function extracts a table from a DrissionPage element and returns it as a pandas DataFrame.
        import pandas as pd
        
        thead=table_ele.ele('t:thead')
        tr=thead.ele('t:tr')

        headers = [th.text.strip() for th in tr.eles('t:th')][1:]
        # print(headers)

        rows = []
        tbody = table_ele.ele('t:tbody')
        for tr in tbody.eles('t:tr'):
            row = [td.ele('t:div').text for td in tr.eles('t:td')][1:]
            rows.append(row)
            # print(rows)

        df = pd.DataFrame(rows,columns=headers)
        
        return df