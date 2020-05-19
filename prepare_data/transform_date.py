from datetime import datetime
import re


def transform_date(date_string):
    """

    :param date_string: str
    :return: a reformed date and add in database
    """
    try:
        if re.match(r"[A-z]", date_string[0]):
            try:
                date = str(datetime.strptime(date_string, "%B %d, %Y")).split()[0]

            except ValueError:
                date = "2020-04-01"

        elif re.match(r"[A-я]", date_string[0]) or not date_string[3].isdigit():
            en_months = ["January", "February", "March", "April", "May", "June",
                         "July", "August", "September", "October", "November", "December"]

            ua_months = ["січень", "лютий", "березень", "квітень", "травень", "червень",
                         "липень", "серпень", "вересень", "жовтень", "листопад", "грудень"]

            ru_months = ["январь", "февраль", "март", "апрель", "май", "июнь",
                         "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]

            date = str(date_string).split()[:-2]

            try:
                month = date[1][:3].lower()
            except IndexError:
                date = str(date_string).split()[:-1]
                month = date[1][:3].lower()

            month_index = 0
            if re.match(r"[A-я]", date_string[0]):
                month = date[0][:3].lower()

            flag_find_month = 0
            for i in range(len(ua_months)):
                if ua_months[i][:3] == month:
                    month_index = i
                    flag_find_month = 1
                    break

            if flag_find_month != 1:
                month = date[1][:3].lower()

                for i in range(len(ru_months)):
                    if ru_months[i][:3] == month:
                        month_index = i
                        break

            if re.match(r"[A-я]", date_string[0]):
                date[0] = en_months[month_index]

                if "2020" not in date_string and "2019" not in date_string and \
                        "2018" not in date_string:
                    date.append("2020")
                    date = " ".join(date)

                    date = str(datetime.strptime(date, "%B %d %Y")).split()[0]
                else:
                    date = " ".join(date)

                    date = str(datetime.strptime(date, "%B  %d, %Y")).split()[0]

            else:
                date[1] = en_months[month_index]

                if "2020" not in date_string and "2019" not in date_string and \
                        "2018" not in date_string:
                    date.append("2020")

                date = " ".join(date)

                date = str(datetime.strptime(date, "%B %d %Y")).split()[0]

        elif date_string[:4] == "2020" or date_string[:4] == "2019" or date_string[:4] == "2018":
            date = date_string[:date_string.find("T")]

        else:
            date = date_string.split(",")[1]
            date = date.split(".")
            date[0] = date[0].strip()
            date[2], date[0] = date[0], date[2]
            date = "-".join(date)
            date = date.strip()
        return date

    except Exception as e:
        print("ERROR_____________________", str(e))
        return date_string
