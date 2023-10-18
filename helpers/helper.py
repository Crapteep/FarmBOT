import re

class Helper:
    @staticmethod
    def regular_expression(data, rule_pattern):
        match = re.search(rule_pattern, data)

        if match:
            value = match.group(1)
            return value
        else:
            return None
    
    @staticmethod
    def response(farm, position, message):
        rsp = {"farm": farm,
                "position": position,
                "message": message}
        print(rsp)